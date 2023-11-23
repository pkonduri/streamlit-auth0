def hide_streamlit_footer_css():
    return """
    <style>
    [data-testid="stToolbar"] {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    </style>
    """


def center_content_on_mobile_css():
    return """
    <style>
    .center-content {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    @media (max-width: 768px) {
        .center-on-mobile {
            /* Additional mobile-specific styles if needed */
        }
    }
    </style>
    """


def user_status_button_css(is_premium_user):
    button_color = "#39FF14" if is_premium_user else "#f44336"
    button_hover_color = "#28a745" if is_premium_user else "#dc3545"
    text_color = 'black' if is_premium_user else 'white'

    return f"""
    <style>
    .user-status-btn {{
        border: none;
        color: {text_color};
        padding: 0.75rem 0.75rem;
        border-radius: 0.25rem;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        background-color: {button_color};
    }}
    .user-status-btn:hover {{
        background-color: {button_hover_color};
    }}
    </style>
    """


def auth_button_css(color):
    button_hover_color = "#3A9F43"
    return f"""
    <style>
        .custom-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            padding: 0.75rem 0.75rem;
            border-radius: 0.25rem;
            margin: 0px;
            line-height: 1.6;
            width: auto;
            user-select: none;
            background-color: {color};
            color: rgb(255, 255, 255);
            border: 1px solid #4CAF50;
            text-decoration: none;
        }}
        .custom-button:hover {{
            background-color: {button_hover_color};
        }}
    </style>
    """


def stripe_redirect_button_after_auth_css():
    color="#FFFF33"
    button_hover_color = "#E6E600"
    return f"""
    <style>
        .redirect-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 400;
            padding: 0.75rem 0.75rem;
            border-radius: 0.25rem;
            margin: 0px;
            line-height: 1.6;
            width: auto;
            user-select: none;
            background-color: {color};
            color: #000;
            text-decoration: none;
        }}
        .redirect-button:hover {{
            background-color: {button_hover_color};
        }}
    </style>
    """

def widen_df():
    return f"""
    <style>
        .stDataFrame {{
            width: 100%;
        }}
    </style>
    """


def div_container_css(bottom_margin: int = 50):
    """Returns the CSS for a centered div container with a specified bottom margin."""
    return f"""
    <style>
    .centered-container {{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: {bottom_margin}px;
    }}
    </style>
    """
