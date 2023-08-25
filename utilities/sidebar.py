import streamlit as st
from datetime import datetime

description = """
**AskDocsAI** is an AI-powered question-answering bot built using OpenAI's GPT models and FAISS vector search. It leverages language embeddings and vector stores to provide efficient and accurate search results.

The bot utilizes the langchain library, which includes prompts, chat models, vector stores, and embeddings. It uses the langchain.prompts module to define system and human message prompts for conversation. The langchain.chat_models module is used to interact with OpenAI's chat models, allowing the bot to generate responses based on the given prompts.

To perform the search operation, **AskDocsAI** employs a FAISS index loaded from the local storage, which is created using OpenAI's embeddings. It uses the index to find the most relevant document chunks based on user queries. The retrieved document chunks are then displayed to the user, along with their metadata.

Once the relevant documents are obtained, **AskDocsAI** uses OpenAI's GPT model to generate answers to user questions. It takes the retrieved documents and the user's query as input to the chat model and generates a response accordingly.

The bot also provides timing information, displaying the elapsed time for the search and answer generation processes.

To use **AskDocsAI**, simply enter your question in the provided text input field, and the bot will retrieve relevant document chunks and generate an answer based on the given query.
"""


def sidebar():
    with st.sidebar:
        if "session_chat_history" in st.session_state:
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
        st.header("About")
        st.write(f"{description}")
