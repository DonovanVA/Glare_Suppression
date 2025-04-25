# U-net glare remover
### 1. (Model training in test.ipynb) Create env + ipykernel to run the jupyter notebook for training
```
conda create -n unet python=3.9 -y
conda activate unet
pip install ipykernel --upgrade
```

Required packages and versions for training:
`tensorflow==2.18.0` 
`scipy==1.14.1` 
`numpy==2.0.2`
`matplotlib==3.10.0`


### 2. Docker 
##### 2.1 Docker build and run image (~1GB container size)
```
docker build -t inference-server .
docker run -d -p 4000:4000  --memory=1g --name inference-active inference-server
```

##### 2.2 get logs
```
docker logs -f inference-active
docker stats inference-active
```

##### 2.3 Alternatively stop and remove the image if error occurs
```
docker stop inference-active 
docker rm inference-active
```

### 3. Tests
##### 3.1 Test endpoint (remote testing):

1. `/predict`
```
curl -X GET  http://localhost:4000/ping
```

2. `/ping`
```
curl -X POST -F "image=@images/002.png" http://localhost:4000/infer
```

3. Script (both `/predict` and `/ping`), image will be saved in /predictions
```
python scripts/test_endpoint.py     
```
