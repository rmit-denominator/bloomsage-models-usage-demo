import os, sys
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)

from dotenv import dotenv_values
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import uvicorn

from machine_learning.pipeline import classify, recommend


config = dotenv_values(".env")
HOST = config["HOST"]
PORT = int(config["PORT"])


app = FastAPI()

app.mount("/images", StaticFiles(directory="data/recommender-database"), name="images")

@app.get("/")
def read_root():
    return {
        "Backend Server Status": "Running",
        "Host": HOST,
        "Port": PORT
    }


@app.post("/upload/")
async def upload_image(image: UploadFile):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    
    image_binary, species = classify(
        image,
        os.path.join(root_dir, "models/clf-cnn")
    )
    recommendations = recommend(
        image, 10,
        os.path.join(root_dir, "data/recommender-database.csv"),
        os.path.join(root_dir, "models/clf-cnn"),
        os.path.join(root_dir, "models/fe-cnn"),
        os.path.join(root_dir, "models/clu-kmeans")
    )
    
    return {
        "species": species,
        "recommendations": recommendations
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
