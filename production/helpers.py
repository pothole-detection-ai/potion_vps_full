import cv2
import base64
import numpy as np

def base64_to_image(base64_string):
    # Check if the string contains a comma and handle accordingly
    if "," in base64_string:
        base64_data = base64_string.split(",")[1]
    else:
        base64_data = base64_string

    try:
        image_bytes = base64.b64decode(base64_data)
    except base64.binascii.Error as e:
        raise ValueError("Invalid base64 string: decoding error") from e
    
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid base64 string: image decoding error")
    return image

def img_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    base64_image = base64.b64encode(buffer).decode('utf-8')
    return base64_image

def base64_to_jpg(base64_string, file_path):
    image = base64_to_image(base64_string)
    cv2.imwrite(file_path, image)

def jpg_to_base64(file_path):
    image = cv2.imread(file_path)
    return img_to_base64(image)
