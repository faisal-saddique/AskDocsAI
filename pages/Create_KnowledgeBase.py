import streamlit as st
from utilities.utils import (
    refined_docs,
    parse_docx,
    parse_readable_pdf,
    parse_xlsx,
    parse_csv,
    parse_json,
    num_tokens_from_string,
    add_vectors_to_FAISS
)

from dotenv import load_dotenv

from utilities.sidebar import sidebar

st.set_page_config(
    page_title='Create KnowledgeBase',
    page_icon='🤖',
    layout='wide',
    initial_sidebar_state='expanded'
)

# sidebar()

# Load environment variables from .env file
load_dotenv()

if "start_fresh" not in st.session_state:
    st.session_state["start_fresh"] = False

def del_uf_history():
    del st.session_state.uploaded_files_history
    del st.session_state.Knowledgebase

if "uploaded_files_history" in st.session_state and not st.session_state["start_fresh"]:
    st.title("Create New KnowledgeBase")
    st.warning("Knowledgebase Already Existing.")
    st.write("Files in Knowledgebase:")
    for file in st.session_state.uploaded_files_history:
        st.info(f"**{file}**: {st.session_state.uploaded_files_history[file]} KBs")
    if st.button("Start Over",on_click=del_uf_history,type="secondary",use_container_width=True):
        st.success("Starting Over again...")
elif "is_Knowledgebase_loaded" in st.session_state and not st.session_state["start_fresh"]:
    st.title("Create New KnowledgeBase")
    st.warning("Knowledgebase Already Existing.")
    if st.button("Start Over",on_click=del_uf_history,type="secondary",use_container_width=True):
        st.success("Starting Over again...")
else:

    st.title("Create New KnowledgeBase")

    accepted_file_types = ["pdf", "csv", "docx", "xlsx", "json"]

    uploaded_files = st.file_uploader("Upload one or more files", accept_multiple_files=True, type=accepted_file_types)

    try:
        if st.button("Create Knowledgebase", use_container_width=True):
            if uploaded_files:
                docs = None
                tot_len = 0

                for file in uploaded_files:
                    file_extension = file.name.split(".")[-1].upper()
                    st.write(f'File: {file.name}, Extension: {file_extension}')
                    file_content = file.read()  # Read the content of the uploaded file
                    
                    if "files_for_download" not in st.session_state:
                        st.session_state.files_for_download = {}
                    if "uploaded_files_history" not in st.session_state:
                        st.session_state.uploaded_files_history = {}
                    st.session_state.uploaded_files_history[f"{file.name}"] = round(file.size / 1024, 2)
                    st.session_state.files_for_download[f"{file.name}"] = file_content

                    if file_extension == 'PDF':
                        if docs is None:
                            docs = parse_readable_pdf(file_content,filename=file.name)
                        else:
                            docs = docs + parse_readable_pdf(file_content,filename=file.name)

                    elif file_extension == 'JSON':
                        if docs is None:
                            docs = parse_json(file_content,filename=file.name)
                        else:
                            docs = docs + parse_json(file_content,filename=file.name)

                    elif file_extension == 'DOCX':
                        if docs is None:
                            docs = parse_docx(file_content,filename=file.name)
                        else:
                            docs = docs + parse_docx(file_content,filename=file.name)

                    elif file_extension == 'XLSX':
                        if docs is None:
                            docs = parse_xlsx(file_content,filename=file.name)
                        else:
                            docs = docs + parse_xlsx(file_content,filename=file.name)
                    
                    elif file_extension == 'CSV':
                        if docs is None:
                            docs = parse_csv(file_content,filename=file.name)
                        else:
                            docs = docs + parse_csv(file_content,filename=file.name)
                    else:
                        raise ValueError("File type not supported!")

                chunked_docs = refined_docs(docs)

                no_of_tokens = num_tokens_from_string(chunked_docs)
                st.write(f"Number of tokens: \n{no_of_tokens}")

                if no_of_tokens:
                    with st.spinner("Creating Knowledgebase..."):
                        st.session_state.Knowledgebase = add_vectors_to_FAISS(chunked_docs=chunked_docs)
                        st.success("Done! Please headover to chatbot to start interacting with your data.")
                        st.session_state["start_fresh"] = False
                else:
                    st.error("No text found in the docs to index. Please make sure the documents you uploaded have a selectable text.")
                    if "uploaded_files_history" in st.session_state:
                        st.session_state.uploaded_files_history = {}
                    st.session_state["start_fresh"] = True
            else:
                st.error("Please add some files first!")
    except Exception as e:
        st.error(f"An error occured while indexing your documents: {e}\n\nPlease fix the error and try again.")