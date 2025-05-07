import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.applications import VGG16
from keras import layers, models, callbacks
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

################################################
# (A) LOAD FER2013 DATA
################################################
data_dir = "/kaggle/input/fer2013-npys"

# We assume you have:
#   train_images.npy (N,224,224,1) or (N,224,224)
#   train_labels.npy (N,)
#   test_images.npy  (M,224,224,1)
#   test_labels.npy  (M,)
train_images = np.load(os.path.join(data_dir, "train_images.npy"))  
train_labels = np.load(os.path.join(data_dir, "train_labels.npy"))  
test_images  = np.load(os.path.join(data_dir, "test_images.npy"))   
test_labels  = np.load(os.path.join(data_dir, "test_labels.npy"))   

num_classes = 7  # FER2013 typically has 7 classes
print(f"Train images: {train_images.shape}, Train labels: {train_labels.shape}")
print(f"Test images: {test_images.shape}, Test labels: {test_labels.shape}")
print(f"Number of classes: {num_classes}")

# "afraid","angry","disgusted","happy","neutral","sad","surprised"

################################################
# (B) PREPROCESSING FUNCTION
################################################
def preprocess_image(image, label):
    """
    1) Resize to 224x224
    2) If grayscale -> replicate to 3 channels
    3) Normalize with ImageNet mean & std
    """
    image = tf.image.resize(image, (224, 224))
    if image.shape[-1] == 1:
        image = tf.repeat(image, repeats=3, axis=-1)
    image = (image - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    return image, label

# Convert integer labels to one-hot
train_labels_oh = keras.utils.to_categorical(train_labels, num_classes)
test_labels_oh  = keras.utils.to_categorical(test_labels, num_classes)

################################################
# (C) BUILD TF.DATA PIPELINES
################################################
batch_size = 8

train_ds = tf.data.Dataset.from_tensor_slices((train_images, train_labels_oh))
test_ds  = tf.data.Dataset.from_tensor_slices((test_images,  test_labels_oh))

train_ds = (
    train_ds
    .shuffle(buffer_size=len(train_images))
    .map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(batch_size)
    .prefetch(tf.data.AUTOTUNE)
)

test_ds = (
    test_ds
    .map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(batch_size)
    .prefetch(tf.data.AUTOTUNE)
)

################################################
# (D) LOAD VGG16 (NO TOP) + CUSTOM HEAD
################################################
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224,224,3))

x = layers.GlobalAveragePooling2D()(base_model.output)
x = layers.Dense(256, activation='relu')(x)
x = layers.Dropout(0.5)(x)
output_layer = layers.Dense(num_classes, activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=output_layer)

################################################
# (E) CALLBACK: SAVE BEST MODEL WHEN val_accuracy>0.60
################################################
class SaveBestAboveThreshold(callbacks.Callback):
    """
    Saves best model once val_accuracy >= 0.60
    If val_accuracy improves further, it overwrites.
    """
    def __init__(self, threshold=0.60, save_path="best_fer2013_tf.h5"):
        super().__init__()
        self.threshold = threshold
        self.save_path = save_path
        self.best_val_acc = 0.0

    def on_epoch_end(self, epoch, logs=None):
        val_acc = logs.get('val_accuracy')
        if val_acc is None:
            return
        if val_acc >= self.threshold and val_acc > self.best_val_acc:
            self.model.save(self.save_path)
            print(f"Epoch {epoch+1}: val_accuracy={val_acc:.4f} >= {self.threshold}, saved best model.")
            self.best_val_acc = val_acc

save_best_callback = SaveBestAboveThreshold(threshold=0.60, save_path="best_fer2013_tf.h5")

################################################
# (F) PHASE 1: 5 epochs, freeze conv base
################################################
base_model.trainable = False
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("=== PHASE 1: (5 epochs) freeze conv base ===")
model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=5,
    callbacks=[save_best_callback],
    verbose=1
)

################################################
# (G) PHASE 2: (20 epochs), unfreeze entire base
################################################
base_model.trainable = True
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("=== PHASE 2: (20 epochs) unfreeze entire VGG16 ===")
model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=20,
    callbacks=[save_best_callback],
    verbose=1
)

################################################
# (H) LOAD BEST CHECKPOINT & FINAL EVAL
################################################
print("\n=== Loading best checkpoint from disk ===")
best_model = keras.models.load_model("best_fer2013_tf.h5")

final_loss, final_acc = best_model.evaluate(test_ds, verbose=1)
print(f"[BEST MODEL] Test Loss: {final_loss:.4f}, Accuracy: {final_acc*100:.2f}%")

predictions = best_model.predict(test_ds)
predicted_classes = np.argmax(predictions, axis=1)

true_classes_all = []
for img_batch, lbl_batch in test_ds:
    lbl_indices = np.argmax(lbl_batch.numpy(), axis=1)
    true_classes_all.append(lbl_indices)
true_classes = np.concatenate(true_classes_all, axis=0)

# Classification report
emotion_names = ["afraid","angry","disgusted","happy","neutral","sad","surprised"]
report = classification_report(true_classes, predicted_classes, target_names=emotion_names)
print(report)
with open("vgg16_fer2013_tf_report.txt", "w") as f:
    f.write(report)

# Confusion Matrix in percentages
cm = confusion_matrix(true_classes, predicted_classes)
cm = cm.astype(np.float32)
row_sums = cm.sum(axis=1, keepdims=True)
cm_perc = (cm / row_sums) * 100.0

print("Confusion Matrix (%):")
print(cm_perc)

plt.figure(figsize=(7,6))
sns.heatmap(cm_perc, annot=True, fmt=".2f", cmap="Blues",
            xticklabels=emotion_names, yticklabels=emotion_names)
plt.title("FER2013 (TensorFlow) - Confusion Matrix (%) [BEST MODEL]")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.savefig("confusion_matrix_fer2013_tf.png", dpi=300, bbox_inches='tight')
plt.show()

print("All done! Best model: best_fer2013_tf.h5")