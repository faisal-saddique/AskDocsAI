import streamlit as st
import zipfile
import os
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv
from utilities.sidebar import sidebar

st.set_page_config(
    page_title='Load KnowledgeBase',
    page_icon='🤖',
    layout='wide',
    initial_sidebar_state='expanded'
)

load_dotenv()
# sidebar()

def is_valid_zip_contents(extracted_dir):
    # Check if the extracted directory contains only two files with the correct name and extensions
    files = os.listdir(extracted_dir)
    if len(files) != 2:
        return False
    
    # Check if both files have the same name
    file_names = [os.path.splitext(file)[0] for file in files]
    if len(set(file_names)) != 1:
        return False
    
    # Check if one file has the extension '.faiss' and the other has '.pkl'
    if ('.faiss' not in files[0] and '.pkl' not in files[1]) and ('.faiss' not in files[1] and '.pkl' not in files[0]):
        return False
    
    return True

# Create a Streamlit page for uploading and loading the zip file
st.title("Upload and Load Existing KnowledgeBase")

# File upload widget
uploaded_zip = st.file_uploader("Upload the zip file containing the KnowledgeBase index:", type=["zip"])

if uploaded_zip:
    # Create a temporary directory to extract the zip contents
    temp_dir = "temp_faiss_Knowledgebase"
    os.makedirs(temp_dir, exist_ok=True)

    # Extract the zip contents to the temporary directory
    with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Check if the extracted directory contains valid contents
    if is_valid_zip_contents(temp_dir):
        embeddings = OpenAIEmbeddings()  # type: ignore
        # Load the FAISS Knowledgebase from the temporary directory
        try:
            if "Knowledgebase" not in st.session_state:
                st.session_state.Knowledgebase = FAISS.load_local(temp_dir, embeddings)
            else:
                st.session_state.Knowledgebase = FAISS.load_local(temp_dir, embeddings)
            st.success("Knowledgebase loaded successfully!")
            st.session_state["is_Knowledgebase_loaded"] = True
            # Now you can use 'new_db' for further operations
        except Exception as e:
            st.error(f"An error occurred while loading the FAISS Knowledgebase: {e}")
    else:
        st.error("Invalid zip file contents. Please make sure the zip contains only two files with the same name and extensions '.faiss' and '.pkl'.")

    # Clean up: Remove the temporary directory
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(temp_dir)