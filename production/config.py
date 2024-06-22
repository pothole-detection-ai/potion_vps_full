import os

# PRODUCTION
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret!")
    MODEL_NAME = "sgd50v8.pt"
    MODEL_FOLDER = "/root/potion_new/models"
    FOLDER_PATH = "images"

# DEVELOPMENT
# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "secret!")
#     MODEL_NAME = "sgd50v8.pt"
#     MODEL_FOLDER = "models"
#     FOLDER_PATH = "images"
