import os
from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph, END
from tools import get_coordinates, get_tourist_spots
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(temperature=0.1,openai_api_key=OPENAI_KEY)


# Define state
from typing import TypedDict, List

class AgentState(TypedDict, total=False):
    city: str
    lat: float
    lon: float
    radius: int
    limit: int
    spots: List[str]  # Or List[Dict[str, Any]] if you're storing full spot details


# Step 1: Get Coordinates
def node_get_coordinates(state: AgentState):
    city = state.get("city")
    if not city:
        return AgentState({**state, "error": "No city provided."})

    coords = get_coordinates(city)
    if "error" in coords:
        return AgentState({**state, "error": coords["error"]})

    return AgentState({**state, **coords})




# Step 2: Get Tourist Spots
def node_get_spots(state: AgentState):
    if "lat" not in state or "lon" not in state:
        return AgentState({**state, "error": "Missing coordinates to fetch spots."})
    lat, lon = state["lat"], state["lon"]
    radius = state.get("radius", 1000)
    limit = state.get("limit", 10)
    spots = get_tourist_spots(lat, lon,radius,limit)
    return AgentState({**state, "spots": spots})

# Step 3: Build Graph
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("get_coordinates", node_get_coordinates)
    graph.add_node("get_spots", node_get_spots)

    graph.set_entry_point("get_coordinates")

    # 🔁 Conditional edge to skip get_spots if error exists
    def route_after_coordinates(state: AgentState):
        return END if "error" in state else "get_spots"

    graph.add_conditional_edges("get_coordinates", route_after_coordinates)
    graph.add_edge("get_spots", END)

    return graph.compile()

