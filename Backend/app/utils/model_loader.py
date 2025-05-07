from app.models_code.pytorch_fer2013 import FER2013PytorchModel
from app.models_code.pytorch_kdef import KDEFPytorchModel
from app.models_code.pytorch_mixed import MixedPytorchModel
from app.models_code.pytorch_nhfi import NHFIPytorchModel
from app.models_code.tf_fer2013 import FER2013TFModel
from app.models_code.tf_kdef import KDEFTFModel
from app.models_code.tf_mixed import MixedTFModel
from app.models_code.tf_nhfi import NHFITFModel


MODEL_CLASSES = {
    'fer2013_pytorch': FER2013PytorchModel,
    'fer2013_tf': FER2013TFModel,
    'kdef_pytorch': KDEFPytorchModel,
    'kdef_tf': KDEFTFModel,
    'mixed_pytorch': MixedPytorchModel,
    'mixed_tf': MixedTFModel,
    'nhfi_pytorch': NHFIPytorchModel,
    'nhfi_tf': NHFITFModel
}

MODEL_CACHE = {}

def preload_models():
    for model_name, model_class in MODEL_CLASSES.items():
        model = model_class()
        model.load_model()
        MODEL_CACHE[model_name] = model
        print(f"Loaded model: {model_name}")

def get_model(model_name):
    if model_name in MODEL_CACHE:
        return MODEL_CACHE[model_name]
    else:
        raise ValueError(f"Model '{model_name}' not found.")