# filename: api_flask.py
from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
import os
import numpy as np
from tensorflow.keras.models import load_model
app = Flask(__name__)

# Load your model here
model = load_model('weights/bright_spot_removal_unet.h5')
def enhance_image(input_image: Image.Image, save_path='predictions') -> Image.Image:
    '''
    Convert image to greyscale, resize, enhance using pretrained .h5 model.
    Save prediction and return enhanced image.
    :param input_image: PIL Image
    :param save_path: folder to save result
    :return: enhanced PIL image
    '''
    os.makedirs(save_path, exist_ok=True)
    
    # Convert to grayscale and resize
    image_gray = input_image.convert("L").resize((512, 512))

    # Prepare for model: [1, 512, 512, 1]
    image_array = np.array(image_gray) / 255.0
    image_array = np.expand_dims(image_array, axis=(0, -1))  # Shape: (1, 512, 512, 1)

    # Predict
    prediction = model.predict(image_array)[0, ..., 0]  # Shape: (512, 512)

    # Convert prediction to image (rescale to [0,255])
    prediction_img = Image.fromarray((prediction * 255).astype(np.uint8))

    # Save prediction
    # filename = "enhanced_image.png"
    # prediction_img.save(os.path.join(save_path, filename))

    return prediction_img
@app.route('/ping', methods=['GET'])
def health():
    '''
    [GET] Health check endpoint
    :return: JSON key-value response
    '''
    return jsonify({"message": "pong"}), 200

@app.route('/infer', methods=['POST'])
def infer():
    '''
    [POST] Inference endpoint
    :return JSON key-value response (image: base64)
    '''
    if 'image' not in request.files:
        return jsonify({"error": "Missing image file in 'image' parameter"}), 400

    file = request.files['image']
    image = Image.open(file.stream)

    enhanced_image = enhance_image(image)
    buffer = io.BytesIO()
    enhanced_image.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return jsonify({"image": img_base64}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

