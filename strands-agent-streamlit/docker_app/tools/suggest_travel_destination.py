from strands import tool
from models.travel_session import TravelSession

session = TravelSession()

@tool
def suggest_travel_destination(agent_name: str, agent_city: str, agent_personality: str, already_suggested: list, suggested_travel_location: str, reasoning: str) -> str:
    """
    Suggest a NEW travel location that hasn't been suggested yet, based on the agent's city and personality.
    
    agent_name: The name of the agent making the suggestion
    agent_city: The city where the agent lives
    agent_personality: Description of the agent's personality and preferences
    already_suggested: List of destinations that have already been suggested by other agents
    suggested_travel_location: The NEW travel destination being suggested (must not be in already_suggested list)
    reasoning: Brief explanation for why this destination was chosen
    """
    session.add_suggestion(agent_name, suggested_travel_location, reasoning)
    return f"Based on living in {agent_city} and personality '{agent_personality}', I suggest {suggested_travel_location} because {reasoning}."