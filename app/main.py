import streamlit as st
import base64
import os

from auth import init_db, login_user, add_user
from components.header import show_header
from components.sidebar import show_sidebar
from components.footer import show_footer
from components.contract_display import analyze_contract

# Initialize DB
init_db()

# Page config
st.set_page_config(
    page_title="LegalLens",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set background image
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .main .block-container {{
            padding-top: 3rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Show background only if not authenticated
if not st.session_state.get("authenticated"):
    set_background("assets/login_bg.jpg")

# Custom CSS for compact and centered fields
st.markdown("""
    <style>
    div[data-baseweb="input"] {
        max-width: 300px;
        margin: 0 auto;
    }
    button[kind="secondary"], button[kind="primary"] {
        max-width: 300px;
        margin: 1rem auto;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# If authenticated, show full dashboard
if st.session_state.get("authenticated"):
    show_header()
    show_sidebar()

    analyze_contract()
    show_footer()
    st.stop()

# ---------------------------
# LOGIN / SIGNUP PAGE (if not authenticated)
# ---------------------------

st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .main-title .lens {
            color: #2F80ED;  /* blue tone, change as needed */
        }
        .centered-subheader {
            text-align: center;
            font-size: 1.5rem;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1.5rem;
        }
    </style>

    <div class="main-title">
        Legal<span class="lens">Lens</span>
    </div>
""", unsafe_allow_html=True)


tabs = st.tabs(["Sign Up", "Sign In", "Continue as Guest"])

# --- SIGN UP ---
with tabs[0]:
    st.markdown('<h3 style="text-align: center;">Create Account</h3>', unsafe_allow_html=True)


    st.markdown('<div style="text-align: center;">Username</div>', unsafe_allow_html=True)
    new_user = st.text_input("", key="signup_user")

    st.markdown('<div style="text-align: center;">Email</div>', unsafe_allow_html=True)
    new_email = st.text_input("", key="signup_email")

    st.markdown('<div style="text-align: center;">Password</div>', unsafe_allow_html=True)
    new_pass = st.text_input("", type="password", key="signup_pass")

    st.markdown('<div style="text-align: center;">Confirm Password</div>', unsafe_allow_html=True)
    confirm_pass = st.text_input("", type="password", key="signup_conf")

    if st.button("Sign Up"):
        if new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif len(new_pass) < 5 or len(new_pass) > 15 or not any(c in "!@#$%^&*" for c in new_pass):
            st.warning("Password must be 5–15 characters and include a special character.")
        else:
            try:
                add_user(new_user, new_pass, new_email)
                st.success("Account created successfully! Please sign in.")
            except:
                st.error("Username already exists.")

# --- SIGN IN ---
with tabs[1]:
    st.markdown('<h3 style="text-align: center;">Sign In</h3>', unsafe_allow_html=True)


    st.markdown('<div style="text-align: center;">Username</div>', unsafe_allow_html=True)
    user = st.text_input("", key="login_user")

    st.markdown('<div style="text-align: center;">Password</div>', unsafe_allow_html=True)
    pwd = st.text_input("", type="password", key="login_pass")

    if st.button("Sign In"):
        if login_user(user, pwd):
            st.session_state["authenticated"] = True
            st.session_state["username"] = user
            st.rerun()
        else:
            st.error("Invalid username or password.")


with tabs[2]:
    st.markdown('<div class="centered-subheader">Continue as Guest</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    if st.button("Continue"):
        st.session_state["authenticated"] = True
        st.session_state["username"] = "Guest"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

