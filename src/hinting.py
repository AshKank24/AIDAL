# main_logic.py

import os
import traceback
import sys
from io import StringIO
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI"))
class Config:
    APP_TITLE = "CereCode"
    MODEL_NAME = "gemini-1.5-pro"

config = Config()
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
            raise ValueError("Empty response received from AI model")
    except Exception as e:
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
        raise

def run_user_code(code):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    try:
        exec(code)
        sys.stdout = old_stdout
        return redirected_output.getvalue()
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error: {str(e)}"