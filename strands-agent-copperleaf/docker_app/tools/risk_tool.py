import random
from typing import List, Dict, Any
from strands import tool
from .asset_tool import assets
from authorization import user_permissions
from context_storage import save_risk_scores

@tool
def analyze_risk(asset_ids: List[str], horizon_months: int = 12, user: str = "User 1") -> Dict[str, Any]:
    """Analyze risk for given asset IDs with specified time horizon"""
    
    # Check user permissions
    # In production, this would likely involve checking a database or an external service
    # In AWS/Azure, this can be done via IAM roles/groups with respective policies for RBAC
    # Here we use a simple dictionary for demonstration
    # For example, using the logged user's session token/API key we can fetch permissions
    # Alternatively, instead of checking for permissions here, we pass that bearer token to the API call
    permissions = user_permissions.get(user, [])
    if "FULL_RISK_SERVICE" not in permissions:
        return {"success": False, "error": "Sorry, user does not have access to risk analysis service"}
    
    risk_analysis = []
    for asset_id in asset_ids:
        asset = assets.get(asset_id)
        if asset:
            if asset.value < 500000:
                risk_score = random.uniform(0, 0.3)
            elif asset.value > 1000000:
                risk_score = random.uniform(0.5, 1.0)
            else:
                risk_score = random.uniform(0.3, 0.5)
            
            risk_analysis.append({
                "assetId": asset_id,
                "riskScore": round(risk_score, 3),
                "horizonMonths": horizon_months
            })
    
    # Save risk scores to context
    risk_scores = {item["assetId"]: item["riskScore"] for item in risk_analysis}
    save_risk_scores(risk_scores)
    
    return {"success": True, "data": {"riskAnalysis": risk_analysis}}