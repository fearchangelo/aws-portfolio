from typing import List
from strands import tool
from models.travel_session import TravelSession

session = TravelSession()

@tool
def pick_travel_destination(agent_name: str, destinations: List[str], chosen_destination: str, reason: str) -> str:
    """
    Pick a travel destination from a list of options (excluding the one the agent proposed).
    
    agent_name: The name of the agent making the choice
    destinations: List of available destinations to choose from
    chosen_destination: The destination the agent chooses
    reason: Brief explanation for the choice
    """
    session.add_choice(agent_name, chosen_destination, reason)
    return f"I choose {chosen_destination} because {reason}"