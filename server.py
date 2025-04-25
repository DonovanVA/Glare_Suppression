# filename: api_flask.py
from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
from model_unet_tf import build_unet,unet_inference
app = Flask(__name__)


# Initialize and build the model
model = build_unet(input_shape=(512, 512, 1))

# Load the weights
model.load_weights('weights/bright_spot_removal_unet.h5')
# Load your model here


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

    enhanced_image = unet_inference(image,model)
    buffer = io.BytesIO()
    enhanced_image.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return jsonify({"image": img_base64}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

