import streamlit as st
from src.summarization import summarize_dsa_topic

def main():
    st.set_page_config(page_title="DSA Topic Explorer", page_icon="🌟")

    st.title("Data Structures and Algorithms Topic Explorer 🚀")
    st.markdown("Welcome, young programmer! Let's explore the world of DSA together!")

    topic = st.text_input("Enter a DSA topic you want to learn about:", placeholder="e.g., binary search tree")

    if st.button("Explore Topic"):
        if topic:
            with st.spinner(f"Searching for information about {topic}..."):
                results = summarize_dsa_topic(topic)

            st.success(f"Great! Here's what I found about {topic}:")

            for i, result in enumerate(results, 1):
                with st.expander(f"Summary {i}"):
                    st.markdown(f"**Source:** [Link]({result['url']})")
                    st.markdown(result['summary'])
                    st.markdown("---")
                    st.markdown("**What did you learn from this summary? 🤔**")
                    st.text_area("Write your thoughts here:", key=f"thoughts_{i}", height=100)

            st.balloons()
            st.markdown("### Keep exploring and learning! 🌈")
        else:
            st.warning("Please enter a topic to explore.")

    st.sidebar.title("About")
    st.sidebar.info(
        "This app helps you learn about Data Structures and Algorithms (DSA) topics. "
        "Just enter a topic, and we'll fetch summaries from various sources to help you understand it better!"
    )

    st.sidebar.title("Tips")
    st.sidebar.markdown(
        """
        - Start with basic topics like "arrays" or "linked lists"
        - Try searching for specific algorithms like "quicksort" or "dijkstra's algorithm"
        - Don't be afraid to explore complex topics – we'll break them down for you!
        - Write down what you learn in the text areas provided
        """
    )

if __name__ == "__main__":
    main()