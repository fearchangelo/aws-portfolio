import requests
from typing import Dict, Any, Optional
from strands import tool
from authorization import user_permissions

from dataclasses import dataclass

@dataclass
class Asset:
    id: str
    name: str
    portfolioId: str
    value: int

assets = {
    "1": Asset(id="1", name="Building A", portfolioId="p1", value=1_200_000),
    "2": Asset(id="2", name="Parking Garage A", portfolioId="p1", value=750_000),
    "3": Asset(id="3", name="HVAC System A", portfolioId="p1", value=300_000),

    "4": Asset(id="4", name="Manufacturing Plant B", portfolioId="p2", value=4_500_000),
    "5": Asset(id="5", name="Substation B", portfolioId="p2", value=2_200_000),
    "6": Asset(id="6", name="Cooling Tower B", portfolioId="p2", value=1_100_000),
    "7": Asset(id="7", name="Backup Generator B", portfolioId="p2", value=650_000),

    "8": Asset(id="8", name="Office C", portfolioId="p3", value=900_000),
    "9": Asset(id="9", name="Data Center C", portfolioId="p3", value=6_800_000),

    "10": Asset(id="10", name="Pipeline D", portfolioId="p4", value=3_200_000),
    "11": Asset(id="11", name="Pump Station D", portfolioId="p4", value=1_500_000),
    "12": Asset(id="12", name="Valve Network D", portfolioId="p4", value=850_000),

    "13": Asset(id="13", name="Warehouse E", portfolioId="p5", value=1_100_000),

    "14": Asset(id="14", name="Retail Store F", portfolioId="p6", value=700_000),
    "15": Asset(id="15", name="POS Infrastructure F", portfolioId="p6", value=250_000),

    "16": Asset(id="16", name="Wind Turbine G", portfolioId="p7", value=2_800_000),
    "17": Asset(id="17", name="Transformer G", portfolioId="p7", value=1_300_000),
    "18": Asset(id="18", name="Control System G", portfolioId="p7", value=600_000),

    "19": Asset(id="19", name="Water Treatment Plant H", portfolioId="p8", value=5_500_000),
    "20": Asset(id="20", name="Filtration Unit H", portfolioId="p8", value=1_200_000),
    "21": Asset(id="21", name="Chemical Storage H", portfolioId="p8", value=900_000),
    "22": Asset(id="22", name="Monitoring Sensors H", portfolioId="p8", value=350_000),

    "23": Asset(id="23", name="Office Tower I", portfolioId="p9", value=7_200_000),
    "24": Asset(id="24", name="Elevator Systems I", portfolioId="p9", value=1_600_000),

    "25": Asset(id="25", name="Logistics Hub J", portfolioId="p10", value=3_900_000),
}

@tool
def get_assets(portfolio_id: Optional[str] = None, asset_id: Optional[str] = None, user: str = "User 1") -> Dict[str, Any]:
    """Get assets from portfolio, optionally filtered by portfolio ID or get specific asset by ID"""
    
    # Check user permissions
    permissions = user_permissions.get(user, [])
    if "FULL_ASSETS_SERVICE" not in permissions and "RESTRICTED_ASSETS_SERVICE" not in permissions:
        return {"success": False, "error": "Sorry, user does not have access to asset service"}
    
    if "RESTRICTED_ASSETS_SERVICE" in permissions:
        if portfolio_id and portfolio_id[1:].isdigit() and int(portfolio_id[1:]) % 2 != 0:
            return {"success": False, "error": f"Sorry, user does not have access to data on portfolio {portfolio_id}"}
    
    if asset_id:
        asset = assets.get(asset_id)
        if asset:
            return {"success": True, "data": {"id": asset.id, "name": asset.name, "portfolioId": asset.portfolioId, "value": asset.value}}
        else:
            return {"success": False, "error": "Asset not found"}
    
    filtered_assets = []
    for asset in assets.values():
        if not portfolio_id or asset.portfolioId == portfolio_id:
            # Filter out odd portfolios for restricted users
            if "RESTRICTED_ASSETS_SERVICE" in permissions and asset.portfolioId[1:].isdigit() and int(asset.portfolioId[1:]) % 2 != 0:
                continue
            filtered_assets.append({"id": asset.id, "name": asset.name, "portfolioId": asset.portfolioId, "value": asset.value})
    
    return {"success": True, "data": filtered_assets}