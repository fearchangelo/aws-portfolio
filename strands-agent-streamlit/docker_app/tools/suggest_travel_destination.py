from strands import tool
from models.travel_session import TravelSession

session = TravelSession()

@tool
def suggest_travel_destination(agent_name: str, agent_city: str, agent_personality: str, suggested_travel_location: str, reasoning: str) -> str:
    """
    Suggest a travel location based on the agent's city and personality.
    
    agent_name: The name of the agent making the suggestion
    agent_city: The city where the agent lives
    agent_personality: Description of the agent's personality and preferences
    suggested_travel_location: The travel destination being suggested
    reasoning: Brief explanation for why this destination was chosen
    """
    session.add_suggestion(agent_name, suggested_travel_location, reasoning)
    return f"Based on living in {agent_city} and personality '{agent_personality}', I suggest {suggested_travel_location} because {reasoning}."