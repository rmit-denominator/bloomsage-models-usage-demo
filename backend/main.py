import os, sys
module_path = os.path.abspath(os.path.join('backend'))
if module_path not in sys.path:
    sys.path.append(module_path)

from dotenv import dotenv_values
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn


from ml_pipeline import classify


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


@app.post("/upload/")
async def upload_image(file: UploadFile):
    image, species = classify(file,"models/clf-cnn")
    recommendation = None  # TOOD: Implement this
    
    return {
        "filename": file.filename,
        "species": species
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
