import operator
import os
from typing import Annotated, TypedDict

import psycopg
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph

load_dotenv()


print("Hello Agent!")