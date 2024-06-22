import os

# PRODUCTION
# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "secret!")
#     MODEL_NAME = "sgd50v8.pt"
#     MODEL_FOLDER = "/home/detectionpotholes/models"
#     FOLDER_PATH = "images"

# DEVELOPMENT
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret!")
    MODEL_NAME = "sgd50v8.pt"
    MODEL_FOLDER = "models"
    FOLDER_PATH = "images"
