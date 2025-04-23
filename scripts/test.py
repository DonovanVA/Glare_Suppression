import requests

# The URL of your Flask API endpoint
# health check
url = 'http://localhost:4000/ping'
response = requests.get(url)
print(response.json())
# Specify the path to the image file to be uploaded
#image_path = 'path_to_your_image.png'  # Replace with the actual path to your image
