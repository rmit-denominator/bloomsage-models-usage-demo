import requests
import streamlit as st
import os
import imghdr
import shutil
import tempfile
import pymongo
from io import BytesIO
from dotenv import dotenv_values, load_dotenv


load_dotenv()


config = dotenv_values(".env")
BACKEND_URI = config["BACKEND"]
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")


# Connect to MongoDB
client = pymongo.MongoClient(f"mongodb+srv://admin:{MONGODB_PASSWORD}@cluster0.zuy7zeb.mongodb.net/")
db = client["testdb"]
collection = db["test"]


def main():
    st.title("BloomSage")

    menu = ["Home", "Upload & Archive", "View Archive"]
    option = st.sidebar.selectbox("Menu", menu)
    if option == "Home":
        show_home()
    elif option == "Upload & Archive":
        show_upload_archive()
    elif option == "View Archive":
        show_view_archive()


def show_home():
    st.write("Demo Upload and save image with streamlit, Use the navigation bar to select!")


def show_upload_archive():
    st.header("Upload & Archive")
    idx = 0

    uploaded_files = st.file_uploader("Upload your flower images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            try:
                # Create a temporary folder
                temp_folder = tempfile.mkdtemp()

                # Save the content of the uploaded file to a temporary file
                temp_image_path = os.path.join(temp_folder, "temp_image.png")
                with open(temp_image_path, "wb") as temp_file:
                    temp_file.write(uploaded_file.read())
                st.image(uploaded_file, caption="Uploaded image", use_column_width=True)

                image_details = get_image_details(temp_image_path)
                st.write("Image details:")
                st.write(image_details)

                files = {"image": uploaded_file}

                response = requests.post(BACKEND_URI, files=files)

                if response.status_code == 200:
                    result = response.json()
                    st.write("Species:", result["species"])
                    # Assuming result["recommendations"] is a list of image paths
                    image_paths = result["recommendations"]

                    # Prepend the server URL to the image paths
                    server_url = "http://localhost:8000/images/"
                    full_image_urls = [server_url + path for path in image_paths]

                    # Display the images
                    st.image(full_image_urls)
                else:
                    st.error("Failed to receive a valid response.")

                if st.button("Archive image", key=idx):
                    archive_image_mongodb(temp_image_path, image_details, result=result.get("species"))
                    st.success("Image archived successfully!")

                st.success("File uploaded successfully!")

            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
            finally:
                # Delete the temporary folder and its contents
                shutil.rmtree(temp_folder, ignore_errors=True)
            idx += 1


def show_view_archive():
    st.header("View archive")

    archived_images = collection.find({})
    for archived_image in archived_images:
        st.image(BytesIO(archived_image["image"]), caption=f"Size - {archived_image['size in mb']} MB", use_column_width=True)
        st.write(archived_image["result"])
        if st.button(f"Delete Image - {archived_image['size in mb']} MB",
                    key=archived_image['_id']):
            delete_image_mongodb(archived_image['_id'])
            st.success("Image deleted successfully!")
            

def archive_image_mongodb(temp_image_path, image_details, result=None):
    with open(temp_image_path, "rb") as image_file:
        image_bytes = image_file.read()
    # image_bytes = image_to_bytes(image)
    document = {
        "size in mb": image_details["File Size in mb"],
        "format": image_details["Format"],
        "image": image_bytes,
        "result": result,
    }
    collection.insert_one(document)


def get_image_details(image_path):
    size = os.path.getsize(image_path)  # Get file size in bytes
    mb_size = str_to_mb(size)
    image_format = imghdr.what(image_path)  # Get image format using imghdr
    details = {
        "File Size in mb": mb_size,
        "Format": image_format,
        # Add more details as needed
    }
    return details


def str_to_mb(string_size):
    bytes_size = int(string_size)
    return bytes_to_mb(bytes_size)


def bytes_to_mb(bytes_size):
    return round(bytes_size / (1024 * 1024), 2)


def delete_image_mongodb(image_id):
    collection.delete_one({"_id": image_id})


if __name__ == '__main__':
    main()
