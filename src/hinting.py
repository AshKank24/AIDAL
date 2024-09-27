import streamlit as st
import os
import logging
import traceback
from dotenv import load_dotenv
from streamlit_ace import st_ace
import google.generativeai as genai
import sys
from io import StringIO

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    APP_TITLE = "CereCode"
    MODEL_NAME = "gemini-1.5-pro"
    
    ACE_EDITOR_CONFIG = {
        "placeholder": "Write your Python code here...",
        "language": "python",
        "theme": "monokai",
        "keybinding": "vscode",
        "font_size": 14,
        "tab_size": 4,
        "show_gutter": True,
        "show_print_margin": True,
        "wrap": True,
        "auto_update": True,
        "key": "code_editor"
    }

config = Config()

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI"))
model = genai.GenerativeModel(model_name=config.MODEL_NAME)
chat_session = model.start_chat(history=[])

def generate_coding_question(previous_questions):
    prompt = f"""Generate a Python coding question focused on data structures and algorithms. 
    Follow these guidelines:
    1. The question should be clear, concise, and suitable for intermediate programmers.
    2. Include a brief problem description and any necessary constraints.
    3. Specify the expected input and output formats.
    4. The question should be different from and slightly more challenging than these previous questions: {previous_questions}
    5. If this is the first question, start with a relatively simple problem.
    6. Include a diagram or visual representation of the data structure or algorithm if it would help the user and is necessary to understand the question problem.
    7. Provide 2-3 examples of inputs and expected outputs covering all edge cases.
    8. Ensure the question is not too similar to the previous questions.
    9. The question should be related to the topic of data structures and algorithms.
    10. Please state clearly how the user should take input for the code.Should it be from standard input or should it be from a function.

    Format your response as follows:
    Question: [Your generated question here]
    Input Format: [Describe the input format]
    Output Format: [Describe the expected output format]
    Example 1:
    Input: [Provide a sample input]
    Output: [Provide the corresponding output for the sample input]
    Example 2:
    Input: [Provide a sample input]
    Output: [Provide the corresponding output for the sample input]
    Example 3:
    Input: [Provide a sample input]
    Output: [Provide the corresponding output for the sample input]
    """
    
    try:
        response = chat_session.send_message(prompt)
        if response and response.text:
            return response.text
        else:
            logger.error("Empty response received from AI model")
            raise ValueError("Empty response received from AI model")
    except Exception as e:
        logger.error(f"Error generating question: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def check_user_code(user_code, question):
    prompt = f"""Analyze the following Python code for the given question:

    Question: {question}

    User's Code:
    {user_code}

    Determine if the code correctly solves the problem. Respond with only one of these two options:
    1. "Correct: The code solves the problem correctly."
    2. "Incorrect: The code does not solve the problem correctly."

    Then also provide a test case on which the code fails if it does not pass.
    Provide the test case in the following format:
    Test Case:
    Input: [Provide a sample input]
    Expected Output: [Provide the corresponding expected output for the sample input]
    Actual Output: [Provide the actual output from the code]

    Only provide the test case in the above format. Do not provide any additional explanations or details.
    """
    
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error checking code: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def generate_hint(user_code, question, step):
    prompt = f"""The user is working on the following Python coding question:

    {question}

    Their current code is:
    {user_code}

    This is hint number {step} out of 3. Please provide a hint based on the following guidelines:

    1. For hint 1: Provide a general approach or algorithm suggestion.
    2. For hint 2: Give a more specific hint about implementation.
    3. For hint 3: Provide a very obvious hint that almost gives away the solution.

    Keep the hint concise, ideally 1-2 sentences.
    """
    
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating hint: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def run_user_code(code):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    try:
        exec(code)
        sys.stdout = old_stdout
        return redirected_output.getvalue()
    except Exception as e:
        logger.error(f"Error executing user code: {str(e)}")
        sys.stdout = old_stdout
        return f"Error: {str(e)}"

def main():
    st.set_page_config(page_title=config.APP_TITLE, layout="wide")
    st.title(config.APP_TITLE)

    if 'previous_questions' not in st.session_state:
        st.session_state['previous_questions'] = []

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button("🎲 Generate a New Coding Question", key="generate_question"):
            with st.spinner("Generating question..."):
                try:
                    question = generate_coding_question(st.session_state['previous_questions'])
                    if question:
                        st.session_state['question'] = question
                        st.session_state['previous_questions'].append(question)
                        st.session_state['hint_step'] = 0
                    else:
                        st.error("Failed to generate a question. Please try again.")
                except Exception as e:
                    logger.error(f"Error in main while generating question: {str(e)}")
                    logger.error(traceback.format_exc())
                    st.error(f"An error occurred while generating the question: {str(e)}. Please try again.")

        if 'question' in st.session_state:
            st.write("### 📝 Current Question:")
            st.info(st.session_state['question'])

        st.write("### 💻 Your Code:")
        user_code = st_ace(**config.ACE_EDITOR_CONFIG)

        if st.button("▶️ Run Code", key="run_code"):
            if user_code:
                with st.spinner("Running your code..."):
                    output = run_user_code(user_code)
                    st.write("### 🖥️ Output:")
                    st.code(output, language="text")
            else:
                st.warning("Please enter your code to run.")

        if st.button("✅ Check Code", key="check_code"):
            if 'question' in st.session_state and st.session_state['question']:
                if user_code:
                    with st.spinner("Checking your code..."):
                        try:
                            check_result = check_user_code(user_code, st.session_state['question'])
                            st.write("### 🔍 Code Check Result:")
                            st.success(check_result)
                        except Exception as e:
                            logger.error(f"Error checking code: {str(e)}")
                            logger.error(traceback.format_exc())
                            st.error(f"An error occurred while checking your code: {str(e)}. Please try again.")
                else:
                    st.warning("Please enter your code to check.")
            else:
                st.warning("Please generate a question first.")

    with col2:
        st.write("### 💡 Hints")
        if st.button("Get a Hint", key="get_hint"):
            if 'question' in st.session_state and st.session_state['question']:
                if user_code:
                    if 'hint_step' not in st.session_state:
                        st.session_state['hint_step'] = 1
                    elif st.session_state['hint_step'] < 3:
                        st.session_state['hint_step'] += 1
                    else:
                        st.warning("You've reached the maximum number of hints for this question.")

                    if st.session_state['hint_step'] <= 3:
                        with st.spinner("Generating hint..."):
                            try:
                                hint = generate_hint(user_code, st.session_state['question'], st.session_state['hint_step'])
                                st.info(f"Hint {st.session_state['hint_step']}: {hint}")
                            except Exception as e:
                                logger.error(f"Error generating hint: {str(e)}")
                                logger.error(traceback.format_exc())
                                st.error(f"An error occurred while generating the hint: {str(e)}. Please try again.")
                else:
                    st.warning("Please enter your code to get a hint.")
            else:
                st.warning("Please generate a question first.")

        if 'hint_step' in st.session_state and st.session_state['hint_step'] > 0:
            for step in range(1, min(st.session_state['hint_step'], 3) + 1):
                with st.expander(f"Hint {step}"):
                    try:
                        prev_hint = generate_hint(user_code, st.session_state['question'], step)
                        st.write(prev_hint)
                    except Exception as e:
                        logger.error(f"Error generating previous hint: {str(e)}")
                        logger.error(traceback.format_exc())
                        st.error(f"An error occurred while retrieving the previous hint: {str(e)}")

    if st.button("🔄 Reset", key="reset"):
        st.session_state['question'] = None
        st.session_state['hint_step'] = 0
        st.experimental_rerun()

if __name__ == "__main__":
    main()