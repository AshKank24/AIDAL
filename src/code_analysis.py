from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
import os
import streamlit as st
import google.generativeai as genai



from datetime import datetime
import pytz
from duckduckgo_search import DDGS
from langchain_community.tools import DuckDuckGoSearchResults
import requests
from dotenv import load_dotenv

# from pymongo import MongoClient
from datetime import datetime

load_dotenv()

genai.configure(api_key=os.environ["GEMINI"])


model = genai.GenerativeModel(
model_name="gemini-2.0-flash",
# safety_settings = Adjust safety settings
# See https://ai.google.dev/gemini-api/docs/safety-settings
tools='code_execution',
)

chat_session = model.start_chat(
    history=[
    ]
    )
groq_api_key = os.getenv("GROQ")


ddg_search_langchain = DuckDuckGoSearchResults()

@tool
def search(query: str):
    """Searches for a query on the Internet and returns the results, use only when required

    Args:
        query: The query which needs to be searched on the internet
    """

    try:
        # results = DDGS().text(query)
        results = ddg_search_langchain.invoke(query)
        results = chat_session.send_message(query)
        print(query)
    except Exception as e:
        print(e)
        results = chat_session.send_message(query)
        # print(response)
        return results.text
    return str(results.text)

@tool
def get_date_time(place : str = 'Asia/Kolkata'):
    """gets date and time for a place , if no place is mentioned gives the date time for Asia/Kolkata.

    Args:
        place: Place or Region always use 'America/New_York', 'Europe/London', 'Asia/Kolkata' format.
    """
    tz = pytz.timezone(place)
    current_datetime = datetime.now(tz)
    return current_datetime

@tool
def execute_code(code : str):
    """generates the code or executes the code and returns the output.

    Args:
        code : The code which needs to be executed 
    """

    try:
        response = chat_session.send_message("Execute this code and return me the output and your observations on the code and its correctness. \nCODE : \n" + code)
        # print(response)
        if 'executable_code' in response:
            print(str(response.executable_code) + response.text)
            return str(response.executable_code) + response.text
        else:
            return response.text
    except Exception as e:
        return e
        
@tool
def generate_code(query : str):
    """returns the code for a given query , you have to return this code to the user.

    Args:
        query : The query for the code which is to be written
    """

    print('GENERATE CODE CALLED')

    try:
        response = chat_session.send_message("Generate the code for " + query)
        print(response)
        # print(response.executable_code)
        # if 'executable_code' in response:
            # print(str(response.executable_code) + response.text)
        return  response.text
        # else:
            # return response.text
    except Exception as e:
        return e

@tool
def scrape(url: str):
    """Scrapes the contents from a Website on Internet and returns the content, use only when required

    Args:
        url: The  url of the website which needs to be scraped
    """

    try:
        print('SCRAPE CALLED')

        url = 'https://r.jina.ai/' + url
        response = requests.get(url)
        results = response.text

    except Exception as e:
        print(e)
        results = "There are some issues with Search Engine Right Now"
    return str(results)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"You are Aidal, a highly intelligent and helpful assistant designed to follow the Socratic Method in teaching. You specialize in guiding learners through Searching and Sorting Algorithms by offering insightful questions, gentle hints, and thought-provoking guidance rather than providing direct answers.Encourage learners to explore concepts through examples, allowing them to discover solutions on their own. Focus on fostering critical thinking, prompting users to reflect on their assumptions, and guiding them to form their own conclusions. REMEMBER TO SHOW AND USE the data returned from function calls like the GENERATED CODE and RESULTS from the internet. Whenever you say that you are providing something ensure it is mentioned in your response and dont give me your function calls in the response. ",

        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
# print(groq_api_key)
llm = ChatGroq(api_key=groq_api_key,model='qwen-qwq-32b',temperature=0.1)
tools = [get_date_time,search,scrape,execute_code,generate_code]
# Construct the Tools agent
agent = create_tool_calling_agent(llm, tools, prompt)

if 'memory' not in st.session_state:
    st.session_state['memory'] = ChatMessageHistory(session_id = 'test_session')

memory = st.session_state.get('memory')


# # Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools)

agent_executor = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)