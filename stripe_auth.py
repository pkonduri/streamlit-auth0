import streamlit as st
import stripe
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

# local imports
from css_helpers import stripe_redirect_button_after_auth_css, div_container_css

def get_api_key() -> str:
    testing_mode = os.getenv('TESTING_MODE', 'False').strip().lower() == 'true'
    return (
        os.environ["STRIPE_API_KEY_TEST"]
        if testing_mode
        else os.environ["STRIPE_API_KEY"]
    )


def redirect_button(
    text: str,
    customer_email: str,
    payment_provider: str = "stripe",
):
    testing_mode = os.getenv('TESTING_MODE', 'False').strip().lower() == 'true'
    encoded_email = urllib.parse.quote(customer_email)
    if payment_provider == "stripe":
        stripe.api_key = get_api_key()
        stripe_link = (
            os.environ["STRIPE_LINK_TEST"]
            if testing_mode
            else os.environ["STRIPE_LINK"]
        )
        button_url = f"{stripe_link}?prefilled_email={encoded_email}"
    elif payment_provider == "bmac":
        button_url = f"{os.environ['BMAC_LINK']}"
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")


    # Apply the custom redirect button CSS
    st.markdown(stripe_redirect_button_after_auth_css(), unsafe_allow_html=True)

    # # Use the 'redirect-button' class for styling the button
    # st.markdown(
    #     f"""
    #     <a href="{button_url}">
    #         <div class="redirect-button">
    #             {text}
    #         </div>
    #     </a>
    #     """,
    #     unsafe_allow_html=True,
    # )

    # Apply the div container CSS
    st.markdown(div_container_css(), unsafe_allow_html=True)  # Apply the div container CSS

    # Use the 'centered-container' class for the div
    st.markdown(
        f"""
        <div class="centered-container">
            <a href="{button_url}">
                <div class="redirect-button">
                    {text}
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def is_active_subscriber(email: str) -> bool:
    stripe.api_key = get_api_key()
    customers = stripe.Customer.list(email=email)
    try:
        customer = customers.data[0]
    except IndexError:
        return False

    subscriptions = stripe.Subscription.list(customer=customer["id"])
    st.session_state.subscriptions = subscriptions
    return len(subscriptions) > 0

def get_stripe_link():
    # Get the mode from the environment variable
    testing_mode = os.getenv('TESTING_MODE', 'True').lower() == 'true'
    # Return the appropriate Stripe link
    if testing_mode:
        return os.environ['STRIPE_LINK_TEST']
    else:
        return os.environ['STRIPE_LINK']