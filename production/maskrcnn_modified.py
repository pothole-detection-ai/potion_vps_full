import os
import cv2
import torch
import random
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2.data import MetadataCatalog
import numpy as np
import shutil

class MaskRCNNmodified:
    def __init__(self, config_path, model_path):
        self.cfg = get_cfg()
        self.cfg.merge_from_file(config_path)
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # Threshold for detection increased to 0.7
        self.cfg.MODEL.WEIGHTS = model_path
        self.cfg.MODEL.DEVICE = 'cpu'
        self.predictor = DefaultPredictor(self.cfg)

    def detect(self, img):
        outputs = self.predictor(img)
        instances = outputs['instances']
        boxes = instances.pred_boxes.tensor.cpu().numpy()
        masks = instances.pred_masks.cpu().numpy()
        scores = instances.scores.cpu().numpy()
        return boxes, masks, scores

    def detect_full(self, img, output_dir="outputs"):
        frame_height, frame_width = img.shape[:2]
        boxes, masks, scores = self.detect(img)
        os.makedirs(output_dir, exist_ok=True)
        output_data = {
            "total_objects": len(boxes),
            "save_dir_path": "",
            "objects": {}
        }

        img_with_masks = img.copy()
        if masks is not None:
            for mask in masks:
                # Find contours for the mask
                contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                cv2.fillPoly(img_with_masks, contours, (0, 128, 255))

            segmented_img = cv2.addWeighted(img, 0.5, img_with_masks, 0.5, 0)

            text_y_position = 20  # Initial Y position for the top text
            text_x_position = 10  # Initial X position for the top text
            text_line_height = 20  # Line height for text
            max_columns = 4  # Maximum number of columns before wrapping to a new row
            
            add_text_with_background(segmented_img, "Model: MASKRCNN", (10, frame_height - 10))
            for i, (box, mask, score) in enumerate(zip(boxes, masks, scores)):
                color = (0, 255, 0)  # Green color for bounding box
                x, y, x2, y2 = box.astype(int)
                box_w, box_h = x2 - x, y2 - y

                pothole_label = f"Pothole {i + 1}"
                cv2.rectangle(segmented_img, (x, y), (x2, y2), color, 3)
                add_text_with_background(segmented_img, pothole_label, (x, y))

                width_text = f"W{i + 1}: {round(box_w * 0.0264583333, 2)} cm"
                length_text = f"L{i + 1}: {round(box_h * 0.0264583333, 2)} cm"
                distance_text = f"D{i + 1}: {round(distance(box_w, box_h), 2)} m"
                score_text = f"S{i + 1}: {score * 100:.2f}%"

                output_data["objects"][f"potholes_{i + 1}"] = {
                    # "bounding_box": [x, y, x2, y2],
                    # "mask": mask.tolist(),
                    "distance": round(distance(box_w, box_h), 2),
                    "width": round(box_w * 0.0264583333, 2),
                    "length": round(box_h * 0.0264583333, 2),
                    "confidence": round(score * 100, 2)
                }

                text_list = [width_text, length_text, distance_text, score_text]

                for j, text in enumerate(text_list):
                    text_x = text_x_position + (i % max_columns) * (frame_width // max_columns)
                    text_y = text_y_position + (i // max_columns) * text_line_height * 4 + j * text_line_height
                    add_text_with_background(segmented_img, text, (text_x, text_y))

        output_image_path = os.path.join(output_dir, "annotated_result.jpg")
        output_data["save_dir_path"] = output_image_path
        cv2.imwrite(output_image_path, segmented_img)

        return output_data

# Function to calculate distance
def distance(box_w, box_h):
    return (((2 * 3.14 * 180) / (box_w + box_h * 360) * 1000 + 5)) * 0.0254

# Function to add text to an image with background
def add_text_with_background(image, text, position, font_scale=0.5, color=(255, 255, 255), thickness=2, bg_color=(0, 0, 0), bg_opacity=0.7):
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    text_x, text_y = position
    overlay = image.copy()
    cv2.rectangle(overlay, (text_x, text_y - text_size[1] - 5), (text_x + text_size[0], text_y + 5), bg_color, -1)
    cv2.addWeighted(overlay, bg_opacity, image, 1 - bg_opacity, 0, image)
    cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

folder_path = r"images"
output_folder = "outputs"
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
    print(f"Folder '{output_folder}' has been deleted successfully.")

# Usage example
model_path = '/root/potion_new/models/maskrcnn.pth'
config_path = '/root/potion_new/models/config.yml'
image_path = '/root/potion_new/assets/photo2.jpeg'
output_path = '/root/potion_new/assets/photo2_hasil.jpeg'

model = MaskRCNNmodified(config_path, model_path)
# result = model.detect_full(cv2.imread(image_path))
# print(result)

def maskrcnn_detect_image(image_path):
    image = cv2.imread(image_path)
    results = model.detect_full(image)
    return results
