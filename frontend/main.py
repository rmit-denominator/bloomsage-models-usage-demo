import requests
import streamlit as st
import os
from PIL import Image
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
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded image", use_column_width=True)

            image_details = get_image_details(image)
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
                archive_image_mongodb(image, image_details, result=result["species"])
                st.success("Image archived successfully!")

            st.success("File uploaded successfully!")
           
            idx += 1

 
# uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
# if uploaded_file is not None:
#     st.write("File uploaded successfully!")
#     files = {"image": uploaded_file}

#     response = requests.post(BACKEND_URI, files=files)
        
#     if response.status_code == 200:
#         result = response.json()
#         st.write("Species:", result["species"])
#         # Assuming result["recommendations"] is a list of image paths
#         image_paths = result["recommendations"]

#         # Prepend the server URL to the image paths
#         server_url = "http://localhost:8000/images/"
#         full_image_urls = [server_url + path for path in image_paths]

#         # Display the images
#         st.image(full_image_urls)
#     else:
#         st.error("Failed to receive a valid response.")


def show_view_archive():
    st.header("View archive")

    archived_images = collection.find({})
    for archived_image in archived_images:
        st.image(BytesIO(archived_image["image"]), caption=f"Archived Image - {archived_image['width']}x{archived_image['height']}", use_column_width=True)
        st.write(archived_image["result"])
        if st.button(f"Delete Image - {archived_image['width']}x{archived_image['height']}",
                    key=archived_image['_id']):
            delete_image_mongodb(archived_image['_id'])
            st.success("Image deleted successfully!")
            

def archive_image_mongodb(image, image_details, result=None):
    image_bytes = image_to_bytes(image)
    document = {
        "width": image_details["Width"],
        "height": image_details["Height"],
        "format": image_details["Format"],
        "image": image_bytes,
        "result": result,
    }
    collection.insert_one(document)


def image_to_bytes(image):
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format=image.format)
    return img_byte_arr.getvalue()


def get_image_details(image):
    width, height = image.size
    format_type = image.format
    details = {
        "Width": width,
        "Height": height,
        "Format": format_type,
    }
    return details


def delete_image_mongodb(image_id):
    collection.delete_one({"_id": image_id})

if __name__ == '__main__':
    main()
