import os
import requests
from zipfile import ZipFile
from dotenv import dotenv_values


config = dotenv_values(".env")
DATASRC = config["DATASRC"]
MODELSRC = config["MODELSRC"]


def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def unzip_file(zip_filename, extract_dir):
    with ZipFile(zip_filename, "r") as zip_ref:
        zip_ref.extractall(extract_dir)


if __name__ == "__main__":
    data_zip_url = DATASRC
    models_zip_url = MODELSRC
    extract_dir = os.path.dirname(os.path.realpath(__file__))
    data_zip_file = os.path.join(extract_dir, "data.zip")
    models_zip_file = os.path.join(extract_dir, "models.zip")

    print("Fetching BloomSage ML Assets")
    print("Downloading data.zip...")
    download_file(data_zip_url, data_zip_file)
    print("Downloading models.zip...")
    download_file(models_zip_url, models_zip_file)
    print("Extracting files...")
    unzip_file(data_zip_file, extract_dir)
    unzip_file(models_zip_file, extract_dir)

    print("Cleaning up...")
    os.remove(data_zip_file)
    os.remove(models_zip_file)

    print("[ DONE ]")
