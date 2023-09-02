import streamlit as st
import zipfile
import os
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()
# Create a Streamlit page for uploading and loading the zip file

st.title("Upload and Load Existing KnowledgeBase")

# File upload widget
uploaded_zip = st.file_uploader("Upload the zip file containing the KnowledgeBase index:", type=["zip"])

if uploaded_zip:
    # Create a temporary directory to extract the zip contents
    temp_dir = "temp_faiss_index"
    os.makedirs(temp_dir, exist_ok=True)

    # Extract the zip contents to the temporary directory
    with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    embeddings = OpenAIEmbeddings()  # type: ignore
    # Load the FAISS index from the temporary directory
    try:
        if "index" not in st.session_state:
            st.session_state.index = FAISS.load_local(temp_dir, embeddings)
        else:
            st.session_state.index = FAISS.load_local(temp_dir, embeddings)
        st.success("Index loaded successfully!")
        st.session_state["is_index_loaded"] = True
        # Now you can use 'new_db' for further operations
    except Exception as e:
        st.error(f"An error occurred while loading the FAISS index: {e}")

    # Clean up: Remove the temporary directory
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(temp_dir)
