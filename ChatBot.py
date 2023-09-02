import utils
import openai
from dotenv import load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
import streamlit as st
from utilities.sidebar import sidebar
from streaming import StreamHandler
import uuid

# Import required libraries for different functionalities
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from langchain.chains import RetrievalQA

from langchain.prompts import PromptTemplate

st.title("Ask Docs AI 🤖")

if "session_chat_history" not in st.session_state:
    st.session_state.session_chat_history = []

# Load environment variables from .env file
load_dotenv()

embeddings = OpenAIEmbeddings()


class CustomDataChatbot:

    def __init__(self):
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def create_qa_chain(self):

        prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, politely say that you don't know, don't try to make up an answer. Always end your answer by asking the user if he needs more help.

        ---------------------------
        {context}
        ---------------------------

        Question: {question}
        Friendly Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        chain_type_kwargs = {"prompt": PROMPT}

        # Create a Pinecone vector store using an existing index and OpenAI embeddings
        vectorstore = st.session_state.index

        st.session_state.qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(streaming=True), chain_type="stuff", retriever=vectorstore.as_retriever(), return_source_documents=True,chain_type_kwargs=chain_type_kwargs)
        

    @utils.enable_chat_history
    def main(self):

        user_query = st.chat_input(placeholder="Ask me anything!")

        if user_query:

            utils.display_msg(user_query, 'user')

            with st.chat_message("assistant", avatar="https://e7.pngegg.com/pngimages/139/563/png-clipart-virtual-assistant-computer-icons-business-assistant-face-service-thumbnail.png"):
                st_callback = StreamHandler(st.empty())
                if 'qa' not in st.session_state:
                    st.session_state.qa = None
                    self.create_qa_chain()
                result = st.session_state.qa({"query": user_query}, callbacks=[
                                             st_callback]) 
                with st.expander("See sources"):
                    for doc in result['source_documents']:
                        st.success(f"Filename: {doc.metadata['source']}")
                        st.info(f"\nPage Content: {doc.page_content}")
                        st.json(doc.metadata, expanded=False)
                        if "is_index_loaded" in st.session_state and st.session_state.is_index_loaded:
                            pass
                        else:
                            st.download_button("Download Original File", st.session_state.files_for_download[f"{doc.metadata['source']}"], file_name=doc.metadata[
                                            "source"], mime="application/octet-stream", key=uuid.uuid4(), use_container_width=True)
                st.session_state.messages.append(
                    {"role": "assistant", "content": result['result'], "matching_docs": result['source_documents']})
                
                st.session_state.session_chat_history.append(
                    (user_query, result["result"]))


if __name__ == "__main__":
    if "index" in st.session_state:
        obj = CustomDataChatbot()
        obj.main()
        sidebar()
    else:
        st.warning("Please create a knowledgeBase first!")
