import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory

# Page configuration
st.set_page_config(
    page_title="LM Studio Chatbot",
    page_icon="💬",
    layout="wide",
)

# Initialize session state variables
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 1000
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful AI assistant. Respond thoughtfully and clearly."
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history"
    )
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_llm():
    """Create a new LLM instance with current settings"""
    return ChatOpenAI(
        temperature=st.session_state.temperature,
        max_tokens=st.session_state.max_tokens,
        openai_api_base="http://localhost:1234/v1",
        openai_api_key="not-needed"
    )

def create_chain():
    """Create the conversation chain with current system prompt"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", st.session_state.system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    
    chain = prompt | get_llm() | StrOutputParser()
    return chain

# Main chat interface
st.title("💬 AI Chat Assistant")

# Sidebar settings
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Create tabs for different settings
    tabs = st.tabs(["Basic", "Advanced", "System Prompt"])
    
    # Basic Settings Tab
    with tabs[0]:
        # Temperature control
        new_temp = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Higher values make the output more random, lower values make it more focused"
        )
        if new_temp != st.session_state.temperature:
            st.session_state.temperature = new_temp
    
    # Advanced Settings Tab
    with tabs[1]:
        # Max tokens control
        new_max_tokens = st.number_input(
            "Max Tokens",
            min_value=50,
            max_value=4000,
            value=st.session_state.max_tokens,
            step=50,
            help="Maximum number of tokens in the response"
        )
        if new_max_tokens != st.session_state.max_tokens:
            st.session_state.max_tokens = new_max_tokens
    
    # System Prompt Tab
    with tabs[2]:
        # System prompt customization
        new_system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.system_prompt,
            height=150,
            help="This sets the behavior and role of the AI assistant"
        )
        if new_system_prompt != st.session_state.system_prompt:
            st.session_state.system_prompt = new_system_prompt
            
        # Preset system prompts
        st.divider()
        st.subheader("Preset Prompts")
        if st.button("General Assistant"):
            st.session_state.system_prompt = "You are a helpful AI assistant. Respond thoughtfully and clearly."
            st.experimental_rerun()
        if st.button("Code Expert"):
            st.session_state.system_prompt = "You are an expert programming assistant. Provide clear, well-commented code examples and detailed technical explanations."
            st.experimental_rerun()
        if st.button("Creative Writer"):
            st.session_state.system_prompt = "You are a creative writing assistant. Provide imaginative, engaging, and well-structured responses with attention to narrative and style."
            st.experimental_rerun()
    
    # Clear chat button (outside tabs)
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.memory.clear()
        st.experimental_rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and response
if prompt := st.chat_input("Type your message here..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and show response
    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                # Get chat history
                chat_history = st.session_state.memory.load_memory_variables({})["chat_history"]
                
                # Create and run chain
                chain = create_chain()
                response = chain.invoke({
                    "chat_history": chat_history,
                    "input": prompt
                })
                
                # Display response
                st.markdown(response)
                
                # Update message history and memory
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.memory.save_context(
                    {"input": prompt},
                    {"output": response}
                )
                
        except Exception as e:
            st.error("Error: Could not generate response. Please check if LM Studio is running.")
            st.error(f"Details: {str(e)}")

# Display current settings in the main chat area
with st.expander("Current Settings"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Temperature:** {st.session_state.temperature}")
    with col2:
        st.markdown(f"**Max Tokens:** {st.session_state.max_tokens}")
    with col3:
        st.markdown("**System Prompt:**")
        st.text(st.session_state.system_prompt)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with LangChain and Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
