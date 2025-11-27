from typing import List, Dict, Any, Set

class AssessmentSession:
    def __init__(self):
        self.completed_actions: List[str] = []
        self.correct_actions: Set[str] = set()
        self.red_flag_actions: List[str] = []
        self.conversation_history: List[Dict[str, str]] = []
        self.scenario_active = False
        self.scenario_name = ""
    
    def start_scenario(self, scenario_name: str):
        self.scenario_name = scenario_name
        self.scenario_active = True
        self.completed_actions = []
        self.correct_actions = set()
        self.red_flag_actions = []
        self.conversation_history = []
    
    def add_completed_action(self, action: str):
        if action not in self.completed_actions:
            self.completed_actions.append(action)
    
    def add_correct_action(self, action: str):
        self.correct_actions.add(action)
    
    def add_red_flag_action(self, action: str):
        if action not in self.red_flag_actions:
            self.red_flag_actions.append(action)
    
    def add_conversation(self, role: str, message: str):
        self.conversation_history.append({"role": role, "message": message})
    
    def reset(self):
        self.__init__()
