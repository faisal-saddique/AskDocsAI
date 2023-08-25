import utils
import openai
import tiktoken
import json
from dotenv import load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
import streamlit as st
from utilities.sidebar import sidebar
from streaming import StreamHandler
import uuid
from langchain.memory import StreamlitChatMessageHistory
# Import required libraries for different functionalities
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

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

        # Define the system message template
        system_template = """You are a helpful assistant. Always end your sentence asking your users if they need more help. Use the following pieces of context to answer the users question at the end. 
        If you cannot find the answer from the pieces of context, just say that you don't know, don't try to make up an answer. If the question is a greeting or goodbye, then be flexible and respond accordingly.
        ----------------
        {context}
        ----------------
        
        This is the history of your conversation with the user so far:
        ----------------
        {chat_history}
        ----------------"""

        # Create the chat prompt templates

        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(
                "Question:```{question}```")
        ]

        qa_prompt = ChatPromptTemplate.from_messages(messages)

        # Optionally, specify your own session_state key for storing messages
        msgs = StreamlitChatMessageHistory(key="special_app_key")

        memory = ConversationBufferMemory(
            memory_key="chat_history", chat_memory=msgs)

        # Create a Pinecone vector store using an existing index and OpenAI embeddings
        vectorstore = st.session_state.index

        # Create a ConversationalRetrievalChain for question answering
        st.session_state.qa = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(streaming=True,
                       temperature=0, model="gpt-3.5-turbo"),  # Chat model configuration
            # Use the Pinecone vector store for retrieval
            vectorstore.as_retriever(k=4),
            # Another OpenAI model for condensing questions
            condense_question_llm=OpenAI(temperature=0),
            combine_docs_chain_kwargs={"prompt": qa_prompt},
            # memory=memory,  # Provide the conversation memory
            return_source_documents=True,
        )

    @utils.enable_chat_history
    def main(self):

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        user_query = st.chat_input(placeholder="Ask me anything!")

        if user_query:

            utils.display_msg(user_query, 'user')

            with st.chat_message("assistant", avatar="https://e7.pngegg.com/pngimages/139/563/png-clipart-virtual-assistant-computer-icons-business-assistant-face-service-thumbnail.png"):
                st_callback = StreamHandler(st.empty())
                if 'qa' not in st.session_state:
                    st.session_state.qa = None
                    self.create_qa_chain()
                result = st.session_state.qa({"question": user_query, "chat_history": st.session_state.chat_history}, callbacks=[
                                             st_callback])  # ,"chat_history": st.session_state.history
                with st.expander("See sources"):
                    for doc in result['source_documents']:
                        st.info(f"\nPage Content: {doc.page_content}")
                        st.json(doc.metadata, expanded=False)
                        st.download_button("Download Original File", st.session_state.files_for_download[f"{doc.metadata['source']}"], file_name=doc.metadata[
                                           "source"], mime="application/octet-stream", key=uuid.uuid4(), use_container_width=True)
                st.session_state.messages.append(
                    {"role": "assistant", "content": result['answer'], "matching_docs": result['source_documents']})
                st.session_state.session_chat_history.append(
                    (user_query, result["answer"]))
                # st.warning(st.session_state.session_chat_history)
                st.session_state.chat_history.append(
                    (user_query, result["answer"]))


if __name__ == "__main__":
    if "index" in st.session_state:
        obj = CustomDataChatbot()
        obj.main()
        sidebar()
    else:
        st.warning("Please create a knowledgeBase first!")
