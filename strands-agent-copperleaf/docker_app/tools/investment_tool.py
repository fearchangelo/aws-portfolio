import requests
import json
from typing import List, Dict, Any
from strands import tool
from authorization import user_permissions
from context_storage import get_risk_score

INTERVENTION_TYPES = {
    "Replace": {"cost_multiplier": 1.0, "risk_reduction": 0.40},
    "Preventive Maintenance": {"cost_multiplier": 0.20, "risk_reduction": 0.20},
    "Retain": {"cost_multiplier": 0.0, "risk_reduction": 0.0}
}

@tool
def optimize_investments(candidates: List[Dict[str, Any]], budget: float, horizon_months: int = 24, user: str = "User 1") -> Dict[str, Any]:
    """Optimize investment selection with one intervention type per asset. Each candidate must have: assetId, interventionType, cost, expectedRiskReduction. Available intervention types: Replace (100% cost, 20% risk reduction), Preventive Maintenance (20% cost, 20% risk reduction), Retain (0% cost, 0% risk reduction)"""
    
    # Check user permissions
    # In production, this would likely involve checking a database or an external service
    # In AWS/Azure, this can be done via IAM roles/groups with respective policies for RBAC
    # Here we use a simple dictionary for demonstration
    # For example, using the logged user's session token/API key we can fetch permissions
    # Alternatively, instead of checking for permissions here, we pass that bearer token to the API call
    permissions = user_permissions.get(user, [])
    if "FULL_OPTIMIZATION_SERVICE" not in permissions:
        return {"success": False, "error": "Sorry, user does not have access to investment optimization service"}
    
    # Validate candidates
    for candidate in candidates:
        if not all(key in candidate for key in ["assetId", "interventionType", "cost", "expectedRiskReduction"]):
            return {"success": False, "error": "Each candidate must have assetId, interventionType, cost, and expectedRiskReduction"}
    
    # Group candidates by asset and select best intervention per asset
    asset_groups = {}
    for candidate in candidates:
        asset_id = candidate["assetId"]
        if asset_id not in asset_groups:
            asset_groups[asset_id] = []
        asset_groups[asset_id].append(candidate)
    
    # Select best intervention per asset (highest risk reduction)
    best_per_asset = []
    for asset_id, asset_candidates in asset_groups.items():
        best = max(asset_candidates, key=lambda x: x["expectedRiskReduction"])
        best_per_asset.append(best)
    
    # Sort by highest risk reduction and select within budget
    sorted_candidates = sorted(best_per_asset, key=lambda x: x["expectedRiskReduction"], reverse=True)
    
    selected = []
    total_cost = 0
    
    for candidate in sorted_candidates:
        if total_cost + candidate["cost"] <= budget:
            # Get actual current risk for the asset from context
            initial_risk = get_risk_score(candidate["assetId"])
            final_risk = initial_risk * (1 - candidate["expectedRiskReduction"])
            
            selected_investment = {
                "assetId": candidate["assetId"],
                "interventionType": candidate["interventionType"],
                "cost": candidate["cost"],
                "expectedRiskReduction": candidate["expectedRiskReduction"],
                "initialRisk": initial_risk,
                "finalRisk": final_risk
            }
            selected.append(selected_investment)
            total_cost += candidate["cost"]
    
    return {
        "success": True,
        "data": {
            "selectedInvestments": selected,
            "totalCost": total_cost
        }
    }