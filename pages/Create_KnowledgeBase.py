import streamlit as st
from utilities.utils import (
    refined_docs,
    parse_docx,
    parse_readable_pdf,
    parse_xlsx,
    parse_csv,
    num_tokens_from_string,
    add_vectors_to_FAISS
)
from dotenv import load_dotenv

from utilities.sidebar import sidebar

sidebar()

# Load environment variables from .env file
load_dotenv()

def del_uf_history():
    del st.session_state.uploaded_files_history
    del st.session_state.index

if "uploaded_files_history" in st.session_state:
    st.title("Existing Index")
    for file in st.session_state.uploaded_files_history:
        st.info(f"**{file}**: {st.session_state.uploaded_files_history[file]} KBs")

    if st.button("Start Over",on_click=del_uf_history,type="secondary",use_container_width=True):
        st.success("Starting Over again...")
else:

    st.title("Upload Documents")

    accepted_file_types = ["pdf", "csv", "docx", "xlsx"]

    uploaded_files = st.file_uploader("Upload one or more files", accept_multiple_files=True, type=accepted_file_types)

    try:
        if st.button("Create Database", use_container_width=True):
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

                    # st.write(file_content)

                    if file_extension == 'PDF':
                        if docs is None:
                            docs = parse_readable_pdf(file_content,filename=file.name)
                        else:
                            docs = docs + parse_readable_pdf(file_content,filename=file.name)

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
                    
                    # for doc in docs:
                    #     st.success(doc)

                chunked_docs = refined_docs(docs)

                # for doc in chunked_docs:
                #     st.warning(doc)

                no_of_tokens = num_tokens_from_string(chunked_docs)
                st.write(f"Number of tokens: \n{no_of_tokens}")

                with st.spinner("Creating Index..."):
                    st.session_state.index = add_vectors_to_FAISS(chunked_docs=chunked_docs)
                    st.success("Done! Please headover to chatbot to start interacting with your data.")

    except Exception as e:
        st.error(f"An error occured while indexing your documents: {e}\n\nPlease fix the error and try again.")