import streamlit as st
from datetime import datetime

description = """
**AskDocsAI** is an AI-powered question-answering bot that uses OpenAI's GPT models and FAISS vector search, employing language embeddings and vector stores for accurate search results and document retrieval. It utilizes the langchain library for prompt handling, chat models, and indexing, providing efficient responses to user queries."""


def sidebar():
    with st.sidebar:
        if "session_chat_history" in st.session_state:
            # st.divider()
            # Generate a unique filename using the current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"chat_history_{timestamp}.txt"
            chat_history = st.session_state.session_chat_history
            chat_text = "\n".join(
                [f"Query: {query}\nAnswer: {answer}\n-----" for query, answer in chat_history])
            if not chat_history:
                st.download_button('Download Session Chat', chat_text,
                                   file_name=file_name, use_container_width=True, disabled=True)
            else:
                st.download_button('Download Session Chat', chat_text,
                                   file_name=file_name, use_container_width=True)
        st.divider()
        st.header("About")
        st.write(f"{description}")
