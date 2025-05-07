import os
import sys
from app.models_code.tf_base_class import TFBaseClass

class KDEFTFModel(TFBaseClass):
    def __init__(self):
        super().__init__()
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        self.model_path = os.path.join(base_path, './app/models/emotion_model_tf_kdef.h5')
        self.input_height = 224
        self.input_width = 224
        self.num_channels = 3
