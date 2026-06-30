import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain_core.tools import StructuredTool

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

if API_KEY is None:
    raise ValueError("AVIATIONSTACK_API_KEY not found.")



class FlightInfoInput(BaseModel):
    departure_airport: str = Field(
        description="Departure airport IATA code. Example: DEL"
    )

    arrival_airport: str = Field(
        description="Arrival airport IATA code. Example: NRT"
    )

@tool(args_schema=FlightInfoInput)
def search_flights(
    departure_airport: str,
    arrival_airport: str,
):
    """
    Search live flights between two airports.

    Inputs:
    - departure_airport : IATA code (Example DEL)
    - arrival_airport : IATA code (Example NRT)
    """

    url = "http://api.aviationstack.com/v1/flights"

    params = {
        "access_key": API_KEY,
        "dep_iata": departure_airport,
        "arr_iata": arrival_airport,
        "limit": 5
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


# flight_tool = StructuredTool.from_function(
#     func=search_flights,
#     name="search_flights",
#     description="""
# Search live flights between two airports.

# Inputs:
# - departure_airport : IATA code (Example DEL)
# - arrival_airport : IATA code (Example NRT)
# """,
#     args_schema=FlightInfoInput,
# )