from auth0_component import login_button
from stripe_auth import is_active_subscriber, redirect_button
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

clientId = os.environ['clientId']
domain = os.environ['domain']

button_text = "Login to view all data"

st.title('Welcome to Auth0-Streamlit')

with st.echo():
# Existing login logic...
    user_info = login_button(clientId=clientId, domain=domain, button_text=button_text)
    if user_info:
        st.write(user_info)
        user_email = user_info['email']  # Assuming the email is part of the user_info
        is_subscriber = is_active_subscriber(user_email)

        if is_subscriber:
            st.write(f"User {user_email} is a premium member.")
        else:
            redirect_button("Go Premium!", user_email)

            
if not user_info:
    st.write("Please login to continue")


