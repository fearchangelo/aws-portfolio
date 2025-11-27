from strands import tool
from models.assessment_session import AssessmentSession

session = AssessmentSession()

@tool
def track_action(user_action: str, necessary_action: str = "", is_red_flag: bool = False) -> str:
    """
    Track an action performed by the candidate during the assessment.
    
    user_action: Description of what the user said they would do
    necessary_action: The EXACT necessary action name from the list (e.g., "Check vital signs") if this matches a required action
    is_red_flag: Whether this action is a red flag (incorrect/dangerous)
    """
    session.add_completed_action(user_action)
    
    if is_red_flag:
        session.add_red_flag_action(user_action)
        return f"Action tracked: {user_action} (RED FLAG)"
    elif necessary_action:
        session.add_correct_action(necessary_action)
        return f"Action tracked: {user_action} -> Matches: {necessary_action} (CORRECT)"
    else:
        return f"Action tracked: {user_action}"

