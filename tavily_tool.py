import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.tools import tool
from tavily import TavilyClient
from langchain_core.tools import StructuredTool

load_dotenv()

tavily = TavilyClient()


@tool
def get_itinerary(destination: str, days: int):
    """
    Get a travel itinerary for a given destination and number of days.

    Args:
        destination (str): The travel destination.
        days (int): The number of days for the itinerary.

    Returns:
        str: A travel itinerary in a structured format day and time wise.
    """

    query = f"Travel itinerary for {destination} for {days} days in a structured format day and time wise."

    respone = tavily.search(query=query)

    return respone