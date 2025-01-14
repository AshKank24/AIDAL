import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain_core.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.react.base import ReActDocstoreAgent

# Page configuration
st.set_page_config(
    page_title="LM Studio Agent",
    page_icon="💬",
    layout="wide",
)

# Define tools
@tool ("Lookup")
def text_processor(text: str) -> str:
    """Process text: converts to uppercase, reverses it, and counts characters."""
    result = {
        'uppercase': text.upper(),
        'reversed': text[::-1],
        'length': len(text),
        'vowels': sum(1 for char in text.lower() if char in 'aeiou')
    }
    return f"Text analysis:\nUppercase: {result['uppercase']}\nReversed: {result['reversed']}\nLength: {result['length']}\nVowel count: {result['vowels']}"

@tool ("Search")
def calculator(expression: str) -> str:
    """Calculate basic math expressions safely."""
    try:
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Error: Invalid expression"

# Initialize session state variables
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 1000
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = """You are a helpful AI assistant with access to two tools:
1. LookUp: Analyzes text by converting to uppercase, reversing it, counting length and vowels
2. Search: Performs basic math calculations
Approach tasks step by step and use your tools when needed. Respond thoughtfully and clearly."""
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )

def get_llm():
    """Create a new LLM instance with current settings"""
    return ChatOpenAI(
        temperature=st.session_state.temperature,
        max_tokens=st.session_state.max_tokens,
        openai_api_base="http://localhost:1234/v1",
        openai_api_key="lm-studio"
    )

def create_agent():
    """Create the React agent with tools and current settings"""
    # Define the tools list - exactly two tools as required
    tools = [
        text_processor,
        calculator
    ]
    
    # Create the base prompt
    system_prompt = SystemMessage(
        content=(
            f"{st.session_state.system_prompt}\n\n"
            "When using tools, format your response as follows:\n"
            "Thought: Explain your thought process\n"
            "Action: Tool name to use\n"
            "Action Input: Input for the tool\n"
            "Observation: Tool output\n"
            "... (repeat Thought/Action/Action Input/Observation if needed)\n"
            "Thought: Final thoughts\n"
            "Final Answer: Your final response"
        )
    )
    
    # Create the agent
    agent = ReActDocstoreAgent.from_llm_and_tools(
        llm=get_llm(),
        tools=tools,
        system_message=system_prompt,
        verbose=True
    )
    
    # Create the executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        memory=st.session_state.memory,
        max_iterations=3,
        early_stopping_method="generate",
        handle_parsing_errors=True
    )
    
    return agent_executor

# Main chat interface
st.title("💬 AI Agent Assistant")

# Sidebar settings
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Create tabs for different settings
    tabs = st.tabs(["Basic", "Advanced", "System Prompt"])
    
    # Basic Settings Tab
    with tabs[0]:
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
        new_system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.system_prompt,
            height=150,
            help="This sets the behavior and role of the AI assistant"
        )
        if new_system_prompt != st.session_state.system_prompt:
            st.session_state.system_prompt = new_system_prompt

    # Clear chat button
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
                # Create and run agent
                agent_executor = create_agent()
                response = agent_executor.invoke({
                    "input": prompt
                })
                
                # Display response
                st.markdown(response["output"])
                
                # Update message history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["output"]
                })
                
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
