import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.code_analysis import agent_executor
from code_editor import code_editor

st.set_page_config(layout="wide", page_title="CerebroX - AI Coding Assistant", page_icon="🧠")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I'm CerebroX. How can I assist you with Data Structures and Algorithms?"}
    ]

# LLM function
def llm_function(query):
    response = agent_executor.invoke({"input": query}, config={"configurable": {"session_id": "<foo>"}})
    return response['output']

# Main content area
main_container = st.container(height=600)

# Input container at the bottom
input_container = st.container()

# Layout within main container
with main_container:
    col1, col2 = st.columns([2, 1])

    # Chat Window
    with col1:
        st.header("Chat with CerebroX")
        chat_container = st.container(height=500)
        
        # Display chat messages
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

    # Code Editor
    with col2:
        st.header("Code Editor")
        code = """def example():
    print("Hello, World!")
"""
        editor = code_editor(code, lang="python", height='500px', buttons=[
            {
                "name": "Run",
                "feather": "Play",
                "primary": True,
                "hasText": True,
                "commands": ["submit"],
                "alwaysOn": True,
                "style": {"right": "0.4rem"}
            }
        ])
        
        if editor['type'] == 'submit':
            st.code(editor['text'])  # Display the code
            # Here you would typically execute the code and show the output
            st.write("Code execution placeholder")

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