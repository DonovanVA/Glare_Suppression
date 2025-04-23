# filename: api_flask.py
from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
app = Flask(__name__)

# Load your model here
# model = load_model('model_path')
def enhance_image(input_image: Image.Image) -> Image.Image:
    '''
    Convert image to greyscale, enhance image using model inference (.pt)
    :param input_image: PIL Image
    :return: enhanced image
    '''
   
    return input_image.convert("L")
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

