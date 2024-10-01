import streamlit as st

st.set_page_config(page_title="Multipage App", page_icon="🚀", layout="wide")

st.title("Welcome to the Multipage App")

st.write("""
This application consists of three main sections:
1. Summarizer
2. Code Editor
3. Socrative Learning (Hinting)

Use the sidebar to navigate between these sections.
""")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Summarizer", "Code Editor", "Socrative Learning"])

if page == "Home":
    st.header("Home")
    st.write("This is the main page of our application. Choose a section from the sidebar to get started!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Summarizer")
        st.write("Quickly summarize long texts or documents.")
        if st.button("Go to Summarizer"):
            st.switch_page("pages/summarization_ui.py")

    with col2:
        st.subheader("Code Editor")
        st.write("Write, edit, and run code in various languages.")
        if st.button("Go to Code Editor"):
            st.switch_page("pages/chat_and_code_ui.py")

    with col3:
        st.subheader("Socrative Learning")
        st.write("Interactive learning with hints and guidance.")
        if st.button("Go to Socrative Learning"):
            st.switch_page("pages/hinting_ui.py")

elif page == "Summarizer":
    st.switch_page("pages/summarization_ui.py")
elif page == "Code Editor":
    st.switch_page("pages/chat_and_code_ui.py")
elif page == "Socrative Learning":
    st.switch_page("pages/hinting_ui.py")