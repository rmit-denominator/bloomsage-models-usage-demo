import os, sys
import requests
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
# OPENAI_API_KEY = config["OPENAI_API_KEY"]

app = FastAPI(
    title="ML-BloomSage",
)

app.mount("/images", StaticFiles(directory="data/recommender-database"), name="images")
app.mount("/logo", StaticFiles(directory="machine_learning/logo"), name="logo")

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

@app.post("/openai/")
async def openai_endpoint(species: str):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Say this is a {species}!"}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    return {"chatgpt_response": response.json()['choices'][0]['message']['content']}

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
