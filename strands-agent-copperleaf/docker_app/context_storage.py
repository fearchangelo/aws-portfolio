# Simple in-memory context storage for risk scores
risk_context = {}

def save_risk_scores(asset_risks: dict):
    """Save risk scores to context"""
    risk_context.update(asset_risks)

def get_risk_score(asset_id: str) -> float:
    """Get risk score from context"""
    return risk_context.get(asset_id, 0.5)  # default fallback