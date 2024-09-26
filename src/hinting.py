import streamlit as st
import os
import google.generativeai as genai
from langchain_core.tools import tool
from dotenv import load_dotenv


# Load environment variables (API keys)
load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI"))

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
)

# Create a chat session
chat_session = model.start_chat(
    history=[]  # History is empty at the beginning
)

# Function to generate a coding question via Gemini (PaLM API)
def generate_coding_question(previous_questions):
    try:
        response = chat_session.send_message(f"Generate one simple python coding data structures question. These are the previous questions : {previous_questions}. Keep increasing the difficulty level of the one question you are generating based on the previous questions. Question:")
        return response.text
    except Exception as e:
        return f"Error generating question: {str(e)}"

# Function to check the user's code
def check_user_code(user_code, question):
    try:
        response = chat_session.send_message(
            f"Check the following code for question {question} and tell me if there are any mistakes in:\n{user_code}. Don't give any suggestions to improve it."
        )
        return response.text
    except Exception as e:
        return f"Error checking code: {str(e)}"

# Function to generate a hint for the user
def generate_hint(user_code, question, step):
    try:
        response = chat_session.send_message(
            f"Provide a hint for fixing the following code for question {question} at step {step}:\n{user_code}"
        )
        return response.text
    except Exception as e:
        return f"Error generating hint: {str(e)}"

# Streamlit app for UI
st.title("Coding Practice with Hints")

if 'previous_questions' not in st.session_state:
    st.session_state['previous_questions'] = []

# Step 1: Button to generate a coding question
if st.button("Generate a Coding Question"):
    question = generate_coding_question(st.session_state['previous_questions'])
    st.session_state['question'] = question
    st.session_state['previous_questions'].append(question)
    st.write("### Coding Question:")
    st.write(question)

# Retrieve the generated question from session state if available
if 'question' in st.session_state:
    st.write("### Current Question:")
    st.write(st.session_state['question'])

# Step 2: Text area for user to input code
user_code = st.text_area("Write your code here:", height=200)

# Step 3: Button to check the code
if st.button("Check Code"):
    if user_code:
        # Check the code using Gemini
        check_result = check_user_code(user_code, st.session_state['question'])
        st.write("### Code Check Result:")
        st.write(check_result)
    else:
        st.write("Please enter your code to check.")

# Step 4: Button to provide hints step-by-step
if st.button("Get a Hint"):
    if user_code:
        if 'hint_step' not in st.session_state:
            st.session_state['hint_step'] = 1  # Initialize hint step
        else:
            st.session_state['hint_step'] += 1  # Increment hint step

        hint = generate_hint(user_code, st.session_state['question'], st.session_state['hint_step'])
        st.write(f"### Hint (Step {st.session_state['hint_step']}):")
        st.write(hint)
    else:
        st.write("Please enter your code to get a hint.")
