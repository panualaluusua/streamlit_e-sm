import streamlit as st
from utils import custom_css

# 1. Set Page Config (must be the first Streamlit command)
st.set_page_config(
    page_title="Results Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed" # Set to collapsed to hide by default
)

# 2. Apply Custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Main Title for the whole app
st.title("MIEHET MASTERS TILANNE") # You might want a more general title here

st.markdown("## Welcome! Select a category from the sidebar.")

# Add any other introductory text or images for the main landing page here 