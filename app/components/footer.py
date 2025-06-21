import streamlit as st
from datetime import datetime

def show_footer():
    st.markdown("---")
    footer = f"""
    <div class="footer">
        <div class="footer-content">
            <div>© {datetime.now().year} LegaLens - All Rights Reserved</div>
            <div class="footer-links">
                <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a> | <a href="#">Contact Us</a>
            </div>
        </div>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)