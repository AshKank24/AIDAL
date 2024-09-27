import streamlit as st
from src.code_analysis import agent_executor
from code_editor import code_editor

your_code_string = '''
def hello():
    print('hello')
'''

st.set_page_config(layout="wide")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello , I am CerebroX and I am here to help you with Data Structures and Algorithms"
        }
    ]
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Function to render chat messages
def render_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# LLM function to get the response
def llm_function(query):
    response = agent_executor.invoke({"input": query}, config={"configurable": {"session_id": "<foo>"}})
    return response['output']

# Layout: Two columns for Chat (left) and Code Editor (right)
col1, col2 = st.columns([2, 1])  # Adjust the ratio as needed

# Left Column: Chat Window
with col1:
    st.header("Chat Window")
    render_chat_messages()

# Right Column: Code Editor
with col2:
    st.header("Code Editor")
    # Custom buttons for the code editor
    custom_btns = [
        {
            "name": "Copy",
            "feather": "Copy",
            "hasText": True,
            "alwaysOn": True,
            "commands": ["copyAll", 
                         ["infoMessage", 
                          {
                              "text": "Copied to clipboard!",
                              "timeout": 2500, 
                              "classToggle": "show"
                          }
                         ]
                        ],
            "style": {"right": "0.4rem"}
        },
        {
            "name": "Run",
            "feather": "Play",
            "primary": True,
            "hasText": True,
            "showWithIcon": True,
            "commands": ["submit", ["infoMessage", 
                                    {
                                        "text": "Code Executed!",
                                        "timeout": 2500, 
                                        "classToggle": "show"
                                    }
                                   ]],
            "style": {"bottom": "0.44rem", "right": "0.4rem"}
        }
    ]
    
    # Add code editor with buttons
    response_dict = code_editor(your_code_string, lang="python", height='400px', buttons=custom_btns)

# Chat input area for user message
query = st.chat_input("Enter your message")

# When a new message is entered
if query:
    # Append the user message to the chat history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    
    # Call the LLM function to get the response
    res = llm_function(query)
    
    # Append the LLM response to the chat history
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": res
        }
    )
    
    # Re-render the chat messages dynamically
    render_chat_messages()
    
    # This makes sure Streamlit doesn't cache the previous state and reruns the chat update
    st.experimental_rerun()
