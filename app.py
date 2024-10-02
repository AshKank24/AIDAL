import streamlit as st

st.set_page_config(page_title="Aidal - Ai Driven Algorithmic Learning", page_icon="🚀", layout="wide")

st.title("Welcome to Aidal - Ai Driven Algorithmic Learning.")

# st.write("""
# This application consists of three main sections:
# 1. Summarizer
# 2. Code Editor
# 3. Socrative Learning (Hinting)

# Use the sidebar to navigate between these sections.
# """)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Summarizer", "Chat and learn", "Practice Questions"])

if page == "Home":
    # st.header("Home")
    # st.write("This is the main page of our application. Choose a section from the sidebar to get started!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Summarizer")
        st.write("Quickly summarize long blogs or complex topics")
        if st.button("Go to Summarizer"):
            st.switch_page("pages/summarization_ui.py")

    with col2:
        st.subheader("Chat and learn")
        st.write("Learn Data Structures in any Language you want.")
        if st.button("Go to Chat and learn"):
            st.switch_page("pages/chat_and_code_ui.py")

    with col3:
        st.subheader("Practice Questions")
        st.write("Interactive Practice for DSA Questions with hints and guidance.")
        if st.button("Go to Practice Questions"):
            st.switch_page("pages/hinting_ui.py")

elif page == "Summarizer":
    st.switch_page("pages/summarization_ui.py")
elif page == "Chat and learn":
    st.switch_page("pages/chat_and_code_ui.py")
elif page == "Practice Questions":
    st.switch_page("pages/hinting_ui.py")