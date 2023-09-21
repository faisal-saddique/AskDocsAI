import streamlit as st
from utilities.utils import (
    download_existing_Knowledgebase,
)
from dotenv import load_dotenv
from utilities.sidebar import sidebar

# sidebar()

st.set_page_config(
    page_title='Download KnowledgeBase',
    page_icon='🤖',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Load environment variables from .env file
load_dotenv()

st.title("Download Existing KnowledgeBase")

if "Knowledgebase" in st.session_state:
    if "uploaded_files_history" in st.session_state and not st.session_state["start_fresh"]:
        st.write("Files in Knowledgebase:")
        for file in st.session_state.uploaded_files_history:
            st.info(f"**{file}**: {st.session_state.uploaded_files_history[file]} KBs")
    download_existing_Knowledgebase()
else:
    st.warning("Please create a knowledgeBase first!")