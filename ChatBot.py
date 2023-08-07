from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import utils

from dotenv import load_dotenv
import os
import time
from langchain.embeddings import OpenAIEmbeddings
import streamlit as st
from utilities.sidebar import sidebar
from streaming import StreamHandler

sidebar()

st.title("Ask Docs AI hehe 🤖")

# Load environment variables from .env file
load_dotenv()

embeddings = OpenAIEmbeddings()

class CustomDataChatbot:

    def __init__(self):
        self.openai_model = "gpt-3.5-turbo"

    @st.spinner('Analyzing documents..')
    def setup_qa_chain(self):

        vectordb =  st.session_state.index

        # Define retriever
        retriever = vectordb.as_retriever(
            search_type='mmr',
            search_kwargs={'k':2}
        )

        # Setup memory for contextual conversation        
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True
        )

        llm = ChatOpenAI(
            model_name=os.getenv('MODEL_NAME') or "gpt-3.5-turbo", # type: ignore
            temperature=os.getenv('MODEL_TEMPERATURE') or .3,
            max_tokens=os.getenv('MAX_TOKENS') or 1500,
            streaming=True
        )

        qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory, verbose=True)
        return qa_chain


    @utils.enable_chat_history
    def main(self):

        user_query = st.chat_input(placeholder="Ask me anything!")

        if user_query:
            qa_chain = self.setup_qa_chain()

            utils.display_msg(user_query, 'user')

            with st.chat_message("assistant",avatar="./assets/boom.png"):
                st_cb = StreamHandler(st.empty())
                response = qa_chain.run(user_query, callbacks=[st_cb]) # 
                st.session_state.messages.append({"role": "assistant", "content": response})

template = f"{os.getenv('OPENAI_GPT_INSTRUCTIONS')}" + '\n```{documents}```'

system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_template = '{question}'
human_message_prompt = HumanMessagePromptTemplate.from_template(
    human_template)
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt])

# chain = LLMChain(llm=llm, prompt=chat_prompt)

if __name__ == "__main__":
    obj = CustomDataChatbot()
    obj.main()

    if "index" in st.session_state:

        pass
        
        # query = st.text_input('Enter a question: ')

        # if query:
        #     start_time = time.perf_counter()

        #     st.write("Starting the search operation...")
            
        #     docs = st.session_state.index.similarity_search(query, k=3)

        #     # st.write(num_tokens_from_string(docs))  

        #     with st.expander("Show Matched Chunks"):
        #         for idx, doc in enumerate(docs):
        #             st.write(f"**Chunk # {idx+1}**")
        #             st.write(f"*{doc.page_content}*")
        #             st.json(doc.metadata, expanded=False)

        #     st.write("Found relevant docs, proceeding to make the query...")

            # You can uncomment the line below and disable the answer fetching from the other method to jump to chain method, which you were using initially
            # answer = chain.run(documents=docs, question=query)

            # This section uses chat completion models to generate the results. You can change the model to text-ada-001 or other models to compare the results from them
            # llm_light = OpenAI(model_name="text-davinci-003",
            #                     temperature=settings.OPENAI_TEMPERATURE, openai_api_key=settings.OPENAI_API_KEY)
            # answer = llm_light(
            # f"{settings.OPENAI_GPT_INSTRUCTIONS}/n{query}/n/nUse this context only:/n{docs}")

            # You can uncomment the line below and disable the answer fetching from the other method to jump to GPT-4 chat mode
            # answer = llm(chat_prompt.format_prompt(documents=[doc.page_content for doc in docs], question=query).to_messages()).content

            # end_time = time.perf_counter()
            # st.success(answer)
            # elapsed_time = end_time - start_time
            # st.write(f"\nElapsed time: {round(float(elapsed_time), 3)} secs")

    else:
        st.warning("Please create a knowledgeBase first!")
