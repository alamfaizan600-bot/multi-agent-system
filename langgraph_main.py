import os
from typing import Dict, Any, List, TypedDict
from dotenv import load_dotenv
from httpx import codes
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
load_dotenv()
from tavily import TavilyClient
from flight_tool import search_flights
from tavily_tool import get_itinerary
tavily = TavilyClient()

print("Hello LangGraph!")

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key = os.environ.get("GROQ_API_KEY")
)

class airportCodeOutput(BaseModel):
    departure_airport: str = Field(description="Departure airport IATA code")
    arrival_airport: str = Field(description="Arrival airport IATA code")
    destination: str = Field(description="Destination city name")

def airport_code_tool(userquery: str) -> airportCodeOutput:
    """
    Get the IATA Airport code for the arrival and departure cities using web search from the query given by the user.
    """
    tavily_query = f"Get the IATA Airport code for the arrival and departure cities from the following query: {userquery}. Return the result in a structured format with keys 'departure_airport' and 'arrival_airport' and 'destination'."

    response = tavily.search(query=tavily_query)
    structured_llm = llm.with_structured_output(airportCodeOutput)
    result = structured_llm.invoke(
        f"""
        Using the search results below, extract the airport codes.
        Search Results: {response}
        """
    )

    return result

class TravelState(TypedDict):
    userquery : str
    departure_airport : str
    arrival_airport : str
    destination : str
    flight_options : str
    itinerary : str
    final_response : str

def get_airport_code(state: TravelState):
    codes = airport_code_tool(state['userquery'])
    state["departure_airport"] = codes.departure_airport
    state["arrival_airport"] = codes.arrival_airport
    state["destination"] = codes.destination
    return state

def get_flight_options(state: TravelState):
    flight_options = search_flights(
        departure_airport=state["departure_airport"],
        arrival_airport=state["arrival_airport"]
    )
    state["flight_options"] = flight_options
    return state

def get_itinerary_details(state: TravelState):
    itinerary = get_itinerary(
        destination=state["destination"],
        days=3  #Currently hardcoding this - can be modified afterwards
    )
    state["itinerary"] = itinerary
    return state

def generate_final_response(state: TravelState):
    """
    Generate the final response for the user in a very sleak and structured format. The response should contain the flight options and the itinerary details both in a good presentable manner.
    """
    response = llm.invoke(
        f"""
        You are a professional travel planner. The user has requested a trip from {state['departure_airport']} to {state['arrival_airport']} ({state['destination']}). 
        Here are the flight options: {state['flight_options']}
        Here is the itinerary: {state['itinerary']}
        
        Please generate a final response for the user that includes:
        1. Flight Options
        2. Day-wise Itinerary
        3. Travel Tips
        
        The response should be structured and easy to read.
        """
    )
    
    state["final_response"] = response
    return state

builder = StateGraph(TravelState)

builder.add_node("airport_code", get_airport_code)
builder.add_node("flight_options", get_flight_options)
builder.add_node("itinerary", get_itinerary_details)
builder.add_node("final_response", generate_final_response)

builder.add_edge(START, "airport_code")
builder.add_edge("airport_code", "flight_options")
builder.add_edge("flight_options", "itinerary")
builder.add_edge("itinerary", "final_response")
builder.add_edge("final_response", END)

graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="agent_reasoning_flow.png")

result = graph.invoke(
    {
        "userquery": "I am planning a 3 day trip from Delhi to Sydney. Can you help me with the best flight options and itinerary details?"
    }
)

print(result["final_response"])