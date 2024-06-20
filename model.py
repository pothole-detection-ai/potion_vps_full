import os
from ultralytics import YOLO
from config import Config

def load_model(model_name):
    model_path = os.path.join(Config.MODEL_FOLDER, model_name)
    try:
        return YOLO(model_path)
    except Exception as e:
        print("Error loading model:", e)
        raise

model = load_model(Config.MODEL_NAME)
