import streamlit as st
import streamlit_authenticator as stauth
import base64
from features import fetch_users, menu

def main():
    st.set_page_config(page_title='BloomSage', page_icon="favicon/Logo_BloomSage Logomark.png")
    LOGO_IMAGE = "favicon/Logo_BloomSage Logomark.png"
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(
            """
            <style>
            .container {
                display: flex;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:50px !important;
                color: #f0000 !important;
                padding-top: 75px !important;
            }
            .logo-img {
                float:right;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="container">
                <img class="logo-img" src='https://faithful-adequate-mudfish.ngrok-free.app/logo/Logo_BloomSage.png' width=150">
                <h1 class="logo-text">BloomSage</h1>
            </div>
            """,
            unsafe_allow_html=True
        )   
        st.header("Welcome to our Application!👋")
    try:
        users = fetch_users()
        emails = []
        usernames = []
        passwords = []

        for user in users:
            emails.append(user['key'])
            usernames.append(user['username'])
            passwords.append(user['password'])

        credentials = {'usernames': {}}
        for index in range(len(emails)):
            credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

        Authenticator = stauth.Authenticate(credentials, cookie_name='bloomSage', key='12345', cookie_expiry_days=1)

        email, authentication_status, username = Authenticator.login(':green[Login]', 'sidebar')
 
        info, info1 = st.columns(2)

        if authentication_status is None:
            with info:
                menu(None, authentication_status, None, None)

        if username:
            if username in usernames:
                if authentication_status:
                    # let User see app
                    # Retrieve the email of the authenticated user
                    authenticated_user_email = credentials['usernames'][username]['name']
                    
                    st.sidebar.subheader(f'Welcome {username}')
                    Authenticator.logout('Log Out', 'sidebar')

                    menu(authenticated_user_email, authentication_status, placeholder, username)

                elif not authentication_status:
                    with info:
                        st.sidebar.error('Incorrect Password or username')
                        menu(None, authentication_status, None, None)
                elif authentication_status is None:
                    with info:
                        st.sidebar.warning('Please feed in your credentials')
                        menu(None, authentication_status, None, None)
            else:
                with info:
                    st.sidebar.warning('Username does not exist, Please Sign up')
                    menu(None, authentication_status, None, None)

    except Exception as e:
        # Handle the exception and print its output
        print(f"An exception occurred: {e}")


if __name__ == '__main__':
    main()
