from crewai import Agent, Task, Crew
from tools import get_coordinates, get_tourist_spots
from langchain.chat_models import ChatOpenAI
import os

llm = ChatOpenAI(temperature=0.5)

# Geocoder Agent
geocoder_agent = Agent(
    role="Geocoding Expert",
    goal="Find latitude and longitude for cities",
    backstory="An expert in finding accurate geolocations for given places",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Tourist Agent
tourist_agent = Agent(
    role="Tour Guide",
    goal="Find nearby tourist attractions using coordinates",
    backstory="A passionate traveler who knows all the famous spots around any city",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Tasks
def create_tasks(city_name):
    get_coords_task = Task(
        description=f"Get coordinates for the city: {city_name}",
        expected_output="Latitude and Longitude",
        agent=geocoder_agent,
        tools=[get_coordinates]
    )

    get_places_task = Task(
        description="Find tourist spots using those coordinates",
        expected_output="List of attractions with names and locations",
        agent=tourist_agent,
        tools=[get_tourist_spots],
        context=[get_coords_task]
    )

    return [get_coords_task, get_places_task]

def create_crew(city_name):
    tasks = create_tasks(city_name)
    return Crew(
        agents=[geocoder_agent, tourist_agent],
        tasks=tasks,
        verbose=True
    )
    