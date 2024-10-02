import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.code_analysis import agent_executor
from code_editor import code_editor

st.set_page_config(layout="wide", page_title="Aidal - AI Assistant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I'm Aidal. How can I assist you with Data Structures and Algorithms?"}
    ]

# LLM function
def llm_function(query):
    response = agent_executor.invoke({"input": query}, config={"configurable": {"session_id": "<foo>"}})
    return response['output']

# Main content area
main_container = st.container(height=500)

# Input container at the bottom
input_container = st.container()

# Layout within main container
with main_container:
    col1, col2 = st.columns([2, 1])

    # Chat Window
    with col1:
        st.header("Chat with Aidal")
        chat_container = st.container(height=400)
        
        # Display chat messages
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

    # Code Editor
    with col2:
        st.header("Code Editor")
        code = """
# Use this space to write your code with proper indentation

def hello():
    print("Hello, I am Aidal.")

                """
        editor = code_editor(code, lang="python", height='350px', buttons=[
            {
                "name": "Copy",
                "feather": "Copy",
                "hasText": True,
                "alwaysOn": True,
                "commands": [
                "copyAll",
                [
                    "infoMessage",
                    {
                    "text": "Copied to clipboard!",
                    "timeout": 2500,
                    "classToggle": "show"
                    }
                ]
                ],
                "style": {
                "top": "0rem",
                "right": "0.4rem"
                }
            }
        ])
        
        if editor['type'] == 'submit':
            # st.code(editor['text'])  # Display the code
            # Here you would typically execute the code and show the output
            st.code("Code copied")

# Chat input at the bottom
with input_container:
    query = st.chat_input("Ask a question...")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with chat_container:
            st.chat_message("user").write(query)
        
        with st.spinner("Generating response..."):
            response = llm_function(query)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with chat_container:
            st.chat_message("assistant").write(response)
        
        st.rerun()