from flask import render_template, jsonify, request
from model import model
from config import Config
import helpers
import yolo_v8_modified
import maskrcnn_modified

def register_routes(app):
    @app.route("/yolo")
    def yolo():
        return render_template("index_yolo.html", model_name=Config.MODEL_NAME)
    
    @app.route("/maskrcnn")
    def maskrcnn():
        return render_template("index_maskrcnn.html", model_name=Config.MODEL_NAME)

    @app.route('/detect', methods=['POST'])
    def detect():
        if 'base64_image_string' in request.json and request.json['base64_image_string']:
            base64_image_string = request.json['base64_image_string']
            image_path = Config.FOLDER_PATH + "/uploaded_object.jpg"
            helpers.base64_to_jpg(base64_image_string, image_path)
            
            
            # results = yolo_v8_modified.yolo_detect_image(image_path)
            
            result_yolo = yolo_v8_modified.yolo_detect_image(image_path)
            result_maskrcnn = maskrcnn_modified.maskrcnn_detect_image(image_path)
            # this has key objects, total_objects, save_dir_path
            # sum the key ['objects']['potholes{i}]['confidence'] for each potholes and divide by total_objects, so get the average confidence

            sum_confidence_of_yolo = sum([result_yolo['objects'][f'potholes_{i+1}']['confidence'] for i in range(result_yolo['total_objects'])])
            sum_confidence_of_maskrcnn = sum([result_maskrcnn['objects'][f'potholes_{i+1}']['confidence'] for i in range(result_maskrcnn['total_objects'])])

            # whoever has the highest average confidence, return that result
            if sum_confidence_of_yolo > sum_confidence_of_maskrcnn:
                results = result_yolo
            else:
                results = result_maskrcnn
            
            
            base64_result = helpers.jpg_to_base64("outputs/annotated_result.jpg")
            return jsonify({
                "base64_image_string": base64_result,
                "total_objects": results["total_objects"],
                "objects": results["objects"]
            })
        return jsonify({"error": "parameter base64_image_string tidak boleh kosong!"})
