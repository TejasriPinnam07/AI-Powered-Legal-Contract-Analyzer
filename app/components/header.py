import streamlit as st


import base64

def show_header():
    # Encode the logo image to base64
    with open("assets/logo.png", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
    <style>
    .header-container {{
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 1rem 0;
    }}
    .header-container img {{
        height: 60px;
    }}
    .header-title {{
        font-size: 1.9rem;
        font-weight: 700;
        margin: 0;
    }}
    .header-subtitle {{
        font-size: 1rem;
        color: #555;
        margin-top: 0.3rem;
    }}
    </style>

    <div class="header-container">
        <img src="data:image/png;base64,{encoded_logo}" alt="Logo">
        <div>
            <div class="header-title">LegaLens</div>
            <div class="header-subtitle">AI-powered contract analysis with risk assessment, entity extraction, and summarization</div>
        </div>
    </div>
    <hr>
    """, unsafe_allow_html=True)
