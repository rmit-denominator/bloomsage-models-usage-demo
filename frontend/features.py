import streamlit as st
import streamlit_authenticator as stauth
import requests
import datetime
import re
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
db = client["Bloomsage"]
collection_image = db['Image']
collection_user = db['User']

def insert_user(email, username, password):
    """
    Inserts Users into the DB
    :param email:
    :param username:
    :param password:
    :return User Upon successful Creation:
    """
    date_joined = str(datetime.datetime.now())

    collection_user.insert_one({'key': email, 'username': username, 'password': password, 'date_joined': date_joined})


def insert_user(email, username, password):
    """
    Inserts Users into the DB
    :param email:
    :param username:
    :param password:
    :return User Upon successful Creation:
    """
    date_joined = str(datetime.datetime.now())

    collection_user.insert_one({'key': email, 'username': username, 'password': password, 'date_joined': date_joined})


def fetch_users():
    users = collection_user.find()

    # Process the users as needed
    user_list = list(users)

    return user_list


def get_user_emails():
    """
    Fetch User Emails
    :return List of user emails:
    """
    users = collection_user.find()
    emails = []
    for user in users:
        emails.append(user['key'])
    return emails


def get_usernames():
    """
    Fetch Usernames
    :return List of user usernames:
    """
    users = collection_user.find()
    usernames = []
    for user in users:
        usernames.append(user['key'])
    return usernames


def validate_email(email):
    """
    Check Email Validity
    :param email:
    :return True if email is valid else False:
    """
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$" #tesQQ12@gmail.com

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    """
    Checks Validity of userName
    :param username:
    :return True if username is valid else False:
    """

    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False


def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

        # Additional variable to track the form submission
        form_submitted = st.form_submit_button('Sign Up')

        if form_submitted:
            if not email:
                st.warning('Email is required')
                return

            if not validate_email(email):
                st.warning('Invalid Email')
                return

            if email in get_user_emails():
                st.warning('Email Already Exists')
                return

            if not validate_username(username):
                st.warning('Invalid Username')
                return

            if username in get_usernames():
                st.warning('Username Already Exists')
                return

            if len(username) < 2:
                st.warning('Username Too Short')
                return

            if len(password1) < 6:
                st.warning('Password is Too Short')
                return

            if password1 != password2:
                st.warning('Passwords Do Not Match')
                return

            hashed_password = stauth.Hasher([password2]).generate()
            insert_user(email, username, hashed_password[0])
            st.success('Account created successfully!!')
            st.balloons()


def menu(authenticated_user_email, authentication_status, placeholder, username):
    if not authentication_status:       
        st.write("If you have no account, please sign up!")
        sign_up()
    else: 
        menu = ["Home", "Upload & Archive", "View Archive"]
        option = st.sidebar.selectbox("Menu", menu)
        if option == "Home":
            show_home(placeholder, username)
        elif option == "Upload & Archive":
            show_upload_archive(authenticated_user_email, placeholder)
        elif option == "View Archive":
            show_view_archive(authenticated_user_email, placeholder)


def show_home(placeholder, username):
    
    with placeholder:
            st.header(f"Welcome to BloomSage, {username}!")
    
    st.link_button("Go to Our Ecommerce Website", "http://localhost:5000")

def show_upload_archive(authenticated_user_email, placeholder):
    with placeholder:
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

                    recommendations = result.get("recommendations", {})
                    if recommendations:
                        st.write("Similar Products:")

                        # Create 5 columns for organizing the cards
                        columns = st.columns(2)

                        # Set a fixed height for each card
                        card_height = "500px"

                        for idx1, (image_path, similarity_score) in enumerate(recommendations.items()):
                            # Display each card in a column with some CSS styling
                            with columns[idx1 % 2].container():
                                st.markdown(
                                    f"""
                                    <style>
                                        .card-container {{
                                            border: 1px solid #ddd;
                                            border-radius: 10px;
                                            padding: 10px;
                                            margin: 10px;
                                            text-align: center;
                                            height: {card_height};
                                            display: flex;
                                            flex-direction: column;
                                            justify-content: space-between;
                                        }}
                                        .card-container img {{
                                            max-width: 100%;
                                            border-radius: 8px;
                                            flex: 1; /* Make the image take up available space */
                                        }}
                                        .card-container p {{
                                            margin-top: 8px;
                                        }}
                                        .card-container a {{
                                            text-decoration: none;
                                            color: #3498db;
                                            font-weight: bold;
                                        }}
                                    </style>
                                    <div class="card-container">
                                        <h3>Product {idx1 + 1}</h3>
                                        <img src="http://localhost:8000/images/{image_path}" alt="Product Image" height = 200px>
                                        <p>Similarity Score: {similarity_score}</p>
                                        <a href="http://localhost:5000" target="_blank">View Details</a>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                        displayed_similarity_score = min(similarity_score for similarity_score in recommendations.values())
                        if displayed_similarity_score >= 0.70:
                            st.success(f"Similar products of {result['species']} flower species with minimum similarity score: {displayed_similarity_score}")
                        elif displayed_similarity_score >= 0.50:
                            st.info(f"We could not find similar products of this {result['species']}. But these might be what you are looking for.")
                    else:
                        st.info("No recommendations available.")

                    if st.button("Archive image", key=idx):
                        archive_image_mongodb(temp_image_path, authenticated_user_email, image_details, result=result.get("species"))
                        st.success("Image archived successfully!")
                else:
                    st.error("S")

                st.success("File uploaded successfully!")

            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
            finally:
                # Delete the temporary folder and its contents
                shutil.rmtree(temp_folder, ignore_errors=True)
            idx += 1


def show_view_archive(authenticated_user_email, placeholder):
    with placeholder:
        st.header("View archive")

    archived_images = collection_image.find({"users_id": authenticated_user_email})
    for archived_image in archived_images:
        st.image(BytesIO(archived_image["image"]), caption=f"Size - {archived_image['size in mb']} MB", use_column_width=True)
        st.write(f"Flower Species: {archived_image['result']}")
        if st.button(f"Delete Image - {archived_image['size in mb']} MB",
                    key=archived_image['_id']):
            delete_image_mongodb(archived_image['_id'])
            st.success("Image deleted successfully!")
            

def archive_image_mongodb(temp_image_path,user_email, image_details, result=None):
    with open(temp_image_path, "rb") as image_file:
        image_bytes = image_file.read()
    # image_bytes = image_to_bytes(image)
    document = {
        "users_id": user_email,
        "size in mb": image_details["File Size in mb"],
        "format": image_details["Format"],
        "image": image_bytes,
        "result": result,
    }
    collection_image.insert_one(document)


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
    collection_image.delete_one({"_id": image_id})