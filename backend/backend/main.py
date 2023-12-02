from dotenv import dotenv_values
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn


from backend.ml_pipeline import classify


config = dotenv_values(".env")
HOST = config["HOST"]
PORT = int(config["PORT"])


app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Backend Server Status": "Running",
        "Host": HOST,
        "Port": PORT
    }


@app.post("/upload/")
async def create_upload_file(file: UploadFile):
    image, species = classify(file,"models/clf-cnn")
    recommendation = None  # TOOD: Implement this
    
    return {
        "filename": file.filename,
        "species": species
    }


@app.get("/upload/")
async def main():
    content = """
<body>
<form action="/upload/" enctype="multipart/form-data" method="post">
<input name="image" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
