import requests
import base64 
import os

# Health check
base_url= 'http://localhost:4000'
ping_url = 'http://localhost:4000/ping'
print("URL:"+base_url)
try:
    response = requests.get(ping_url)
    print("/ping response:", response.json())
except Exception as e:
    print("Failed to connect to the server:", e)
    exit()

# Image upload and inference
image_path = './images/002.png'

if not os.path.exists(image_path):
    print("Image file not found:", image_path)
    exit()

with open(image_path, 'rb') as img_file:
    response = requests.post(
        'http://localhost:4000/infer',
        files={'image': img_file}
    )

if response.status_code == 200:
    data = response.json()
    img_data = data['image']

    # Save decoded image
    with open('predictions/result.png', 'wb') as f:
        print("/infer response:",data)
        f.write(base64.b64decode(img_data))
    print("Enhanced image saved as predictions/result.png")
else:
    print("Error:", response.status_code, response.text)
