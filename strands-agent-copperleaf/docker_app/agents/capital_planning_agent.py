from strands import Agent
from strands.models import BedrockModel
from tools import get_assets, analyze_risk, optimize_investments

def create_capital_planning_agent(model: BedrockModel, budget: float, horizon_months: int, user: str = "User 1") -> Agent:
    system_prompt = f"""You are a capital planning assistant with access to portfolio management tools.
Help users analyze assets, assess risks, and optimize investment decisions.
The available budget is ${budget:,.0f} and the time horizon is {horizon_months} months.
The current user is {user}.
Use these values when calling the investment optimization and risk analysis tools.
Always pass the user parameter as "{user}" when calling get_assets.
Only reply to the specific questions asked by the user. Do not ask follow up questions"""
    
    return Agent(
        name="Capital Planning Agent",
        model=model,
        system_prompt=system_prompt,
        tools=[get_assets, analyze_risk, optimize_investments]
    )