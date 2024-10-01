# ui.py

import streamlit as st
from streamlit_ace import st_ace
from main_logic import generate_coding_question, check_user_code, generate_hint, run_user_code

# Initialize session state
if 'previous_questions' not in st.session_state:
    st.session_state['previous_questions'] = []

# UI Configuration
st.set_page_config(page_title="CereCode", layout="wide")
st.title("CereCode")

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
                st.error(f"An error occurred while generating the question: {str(e)}. Please try again.")

    if 'question' in st.session_state:
        st.write("### 📝 Current Question:")
        st.info(st.session_state['question'])

    st.write("### 💻 Your Code:")
    user_code = st_ace(
        placeholder="Write your Python code here...",
        language="python",
        theme="monokai",
        keybinding="vscode",
        font_size=14,
        tab_size=4,
        show_gutter=True,
        show_print_margin=True,
        wrap=True,
        auto_update=True,
        key="code_editor"
    )

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
                            st.error(f"An error occurred while generating the hint: {str(e)}. Please try again.")
            else:
                st.warning("Please enter your code to get hints.")
        else:
            st.warning("Please generate a question first.")
