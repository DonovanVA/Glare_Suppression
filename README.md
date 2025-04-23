# 1. Create env + ipykernel to run jupyter
```
conda create -n tashr python=3.9 -y
conda activate tashr
pip install ipykernel --upgrade
```


# 2. External resources:
Download necessary resources and put in root folder
model:  https://github.com/ChenyangLEI/polarization-reflection-removal/blob/master/VGG_Model/download_VGG.txt
```

```
# 2. Docker 
### 2.1 Docker build and run image
```
docker build -t tashr-server .
docker run -d -p 4000:4000 --name tashr-active tashr-server
```
### 2.2 Alternatively stop and remove the image
```
docker stop tashr-active 
docker rm tashr-active
```
# 3. Tests
### 3.1 Test endpoint (pre docker):
1. /predict
```
curl -X GET  http://localhost:4000/ping
```

2. /ping
```
curl -X POST -F "image=@path_to_image.png" http://localhost:4000/infer
```


# 3.2 Test endpoint (docker):
