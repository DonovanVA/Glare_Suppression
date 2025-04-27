import requests
import base64 
import os

# Health check
base_url= 'http://localhost:4000'
print("URL:"+base_url)
try:
    response = requests.get(base_url+"/ping")
    print("/ping response:", response.json())
except Exception as e:
    print("Failed to connect to the server:", e)
    exit()

# Image upload and inference'
image_path = './images'
if not os.path.exists(image_path):
    print("Image file not found:", image_path)
    exit()
for image in os.listdir(image_path):
    if image.endswith('.png'):
        image_path = os.path.join('./images', image)
        print("Image path:", image_path)

    with open(image_path, 'rb') as img_file:
        response = requests.post(
            base_url+"/infer",
            files={'image': img_file}
        )

        if response.status_code == 200:
            data = response.json()
            img_data = data['image']

            # Save decoded image
            predictions_dir = 'predictions'
            os.makedirs(predictions_dir, exist_ok=True)
            save_image_path_name = predictions_dir+"/"+image.split('.')[0]+"_enhanced.png"
            
            with open(save_image_path_name, 'wb') as f:
                print("/infer response:",data)
                f.write(base64.b64decode(img_data))
            print("Enhanced image saved as predictions/result.png")
            
        else:
            print("Error:", response.status_code, response.text)
