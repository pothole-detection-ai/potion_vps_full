from flask_socketio import emit
from model import model
from config import Config
import helpers
import yolo_v8_modified
import maskrcnn_modified

def register_socketio_handlers(socketio):
    @socketio.on("connect")
    def test_connect():
        print("Connected")
        emit("my response", {"data": "Connected"})

    @socketio.on("image_yolo")
    def receive_image_yolo(base64_image_string):
        if model is not None:
            image_path = Config.FOLDER_PATH + "/uploaded_object.jpg"
            helpers.base64_to_jpg(base64_image_string, image_path)
            results = yolo_v8_modified.yolo_detect_image(image_path)
            base64_result = helpers.jpg_to_base64("outputs/annotated_result.jpg")
            base64_result = f"data:image/jpeg;base64,{base64_result}"
            emit("processed_image_yolo", base64_result)
        else:
            print("Model is not loaded, skipping image processing")
    
    @socketio.on("image_maskrcnn")
    def receive_image_maskrcnn(base64_image_string):
        if model is not None:
            image_path = Config.FOLDER_PATH + "/uploaded_object.jpg"
            helpers.base64_to_jpg(base64_image_string, image_path)
            results = maskrcnn_modified.maskrcnn_detect_image(image_path)
            base64_result = helpers.jpg_to_base64("outputs/annotated_result.jpg")
            base64_result = f"data:image/jpeg;base64,{base64_result}"
            emit("processed_image_maskrcnn", base64_result)
        else:
            print("Model is not loaded, skipping image processing")
