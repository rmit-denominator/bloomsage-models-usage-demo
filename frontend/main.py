import requests
import streamlit as st
from dotenv import dotenv_values

config = dotenv_values(".env")
BACKEND_URI = config["BACKEND"]


st.title("BloomSage")

uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.write("File uploaded successfully!")
    files = {"image": uploaded_file}

    response = requests.post(BACKEND_URI, files=files)
        
    if response.status_code == 200:
        result = response.json()
        st.write("Species:", result["species"])
        st.write("Recommendations:", result["recommendations"])
    else:
        st.error("Failed to receive a valid response.")
