from keras.models import load_model as keras_load_model

def load_model(path):
    """Loads recognizer keras model"""
    return keras_load_model(path)