import operator
import os
from typing import Annotated, TypedDict



import psycopg
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph
from pprint import pprint
from langchain_core.messages import ToolMessage
from langchain.agents import create_agent

from langchain_tavily import TavilySearch
from tavily_tool import get_itinerary
from flight_tool import search_flights

load_dotenv()


print("Hello Agent!")

llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model= "llama-3.3-70b-versatile"
)

# tools = [search_flights]

tools = [get_itinerary, search_flights]

agent = create_agent(
    model=llm,
    tools=tools,
)

prompt = """
    You are a professional travel planner.

    When the user asks for a trip:

    1. ALWAYS use search_flights.
    2. ALWAYS use get_itinerary.
    3. Combine BOTH tool outputs.

    The final response MUST contain:

    ## Flight Options
    Provide the Flight details along with timings.
    ...

    ## Day-wise Itinerary
    Not so detailed itinerary for each day with time and activity.
    ...

    ## Travel Tips

    ...

"""

response = agent.invoke(
    {
        "messages":[
            SystemMessage(content=prompt),
            HumanMessage(content="I am planning a 3 daytrip from Delhi to Sydney. Can you help me with the best flight options and itinerary details?"),
        ]
    }
)

print("Agent Response:")
print(response["messages"][-1].content)