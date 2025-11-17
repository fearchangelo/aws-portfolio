from typing import List, Dict, Any
from collections import Counter

class TravelSession:
    def __init__(self):
        self.data: Dict[str, Dict[str, Any]] = {}
    
    def add_suggestion(self, agent_name: str, destination: str, reasoning: str = ""):
        self.data[agent_name] = {"suggested_travel_location": destination, "suggestion_reasoning": reasoning}
    
    def add_choice(self, agent_name: str, chosen_destination: str, reason: str):
        if agent_name not in self.data:
            self.data[agent_name] = {}
        self.data[agent_name].update({"chosen_destination": chosen_destination, "reason": reason})
    
    def get_all_destinations(self) -> List[str]:
        return [info['suggested_travel_location'] for info in self.data.values()]
    
    def get_other_destinations(self, agent_name: str) -> List[str]:
        return [info['suggested_travel_location'] for name, info in self.data.items() if name != agent_name]
    
    def get_most_chosen(self) -> str:
        choices = [info["suggested_travel_location"] for info in self.data.values() if "suggested_travel_location" in info]
        return Counter(choices).most_common(1)[0][0] if choices else None