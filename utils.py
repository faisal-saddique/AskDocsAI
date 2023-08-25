import os
import random
import streamlit as st
import uuid 

#decorator
def enable_chat_history(func):
    # to clear chat history after swtching chatbot
    current_page = func.__qualname__
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except:
            pass

    # to show chat history on ui
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            if "index" in st.session_state:
            # print(msg["content"])
                with st.chat_message(msg["role"],avatar="https://e7.pngegg.com/pngimages/139/563/png-clipart-virtual-assistant-computer-icons-business-assistant-face-service-thumbnail.png"):
                    st.write(msg["content"])
                    if "matching_docs" in msg:
                        with st.expander("See sources"):
                            for doc in msg['matching_docs']:
                                st.info(f"\nPage Content: {doc.page_content}")
                                st.json(doc.metadata, expanded= False)
                                st.download_button("Download Original File", st.session_state.files_for_download[f"{doc.metadata['source']}"], file_name=doc.metadata["source"], mime="application/octet-stream", key=uuid.uuid4(), use_container_width=True)
        else:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):

    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)