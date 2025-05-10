from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")


import os
from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph, END
from tools import get_coordinates, get_tourist_spots
from dotenv import load_dotenv



llm = ChatOpenAI(temperature=0.1,openai_api_key=OPENAI_KEY)


# Define state
from typing import TypedDict, List

class AgentState(TypedDict, total=False):
    city: str
    lat: float
    lon: float
    spots: List[str]


# Step 1: Get Coordinates
def node_get_coordinates(state: AgentState):
    print("State received in get_coordinates:", state)
    city = state.get("city")
    if not city or city.strip() == "":
        raise ValueError("City name not found or is empty.")
    coords = get_coordinates(city)
    return AgentState({**state, **coords})



# Step 2: Get Tourist Spots
def node_get_spots(state: AgentState):
    lat, lon = state["lat"], state["lon"]
    spots = get_tourist_spots(lat, lon)
    return AgentState({**state, "spots": spots})

# Build LangGraph
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("get_coordinates", node_get_coordinates)
    graph.add_node("get_spots", node_get_spots)

    graph.set_entry_point("get_coordinates")
    graph.add_edge("get_coordinates", "get_spots")
    graph.add_edge("get_spots", END)

    return graph.compile()
