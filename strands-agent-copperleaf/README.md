# AI Agent Portfolio Management System

A Streamlit-based AI agent for portfolio management with, asset tracking, risk analysis, and investment optimization using AWS Strands SDK and AWS Bedrock.

# Deployed on AWS using CDK

Working demo: https://d2sf4cb6s0ooii.cloudfront.net/

## Solution Overview

This application implements an AI agent that provides portfolio management capabilities through a conversational interface:

- **AI Agent**: Built using Strands framework with AWS Bedrock models (Claude 3.5 Haiku, Amazon Nova Lite)
- **Role-Based Access Control**: User permissions system with different service access levels
- **Mock Services**: Asset, Risk, and Investment optimization tools with simulated data
- **Interactive UI**: Streamlit interface with user selection and configuration options

## Configuration & Setup

### Prerequisites
- Python 3.8+
- AWS credentials configured for Bedrock access
- Required Python packages (see requirements.txt)

### Local Development
```bash
cd docker_app
pip install -r requirements.txt
streamlit run app.py
```

### Docker
```bash
cd docker_app
docker-compose up --build
```

### Access the Application
- Web Interface: http://localhost:8501
- Select user (User 1 or User 2) from sidebar dropdown
- Configure budget and time horizon
- Interact with the AI agent through chat

### Sample Usage
- "What assets are in portfolio p1?"
- "Perform a risk assessment on portfolio p2"
- "Optimize portfolio p3"

## User Permissions

### User 1 (Full Access)
- FULL_ASSETS_SERVICE: Access to all portfolios and assets
- FULL_RISK_SERVICE: Can perform risk analysis
- FULL_OPTIMIZATION_SERVICE: Can optimize investments

### User 2 (Restricted Access)
- RESTRICTED_ASSETS_SERVICE: Access only to even-numbered portfolios (p2, p4, p6, p8, p10)
- FULL_RISK_SERVICE: Can perform risk analysis
- No investment optimization access

## Assumptions Made

1. **Mock Data**: All services use simulated data instead of real external APIs
2. **Risk Scoring**: Risk values are randomly generated based on asset values:
   - Assets < $500K: Risk 0-0.3
   - Assets > $1M: Risk 0.5-1.0
   - Assets in between: Risk 0.3-0.5
3. **Portfolio Optimization**: Actions are selected upon these choices:
   - Replace Asset: Costs 100% of the asset, reduces risk by 0.4
   - Preventive Maintenance: Costs 20% of the asset, reduces risk by 0.2
   - Retain Asset: No cost, no risk reduction
4. **Portfolio Access**: Even/odd portfolio restriction is based on numeric suffix (p1, p2, etc.)
5. **User Context**: User selection persists throughout the session and is passed to all tool calls
6. **AWS Bedrock**: Assumes proper AWS credentials and Bedrock model access are configured

## Additional Considerations for Interview Discussion

### Architecture & Design
- **Agentic Orchestrator**: Implemented using Strands SDK (see `capital_planning_agent.py`)
- **Tool Wrappers**: Implemented using Strands SDK with `@tool` decorator (see `asset_tool.py`, `investment_tool.py`, `risk_tool.py`)
- **Mock API Behavior**: Instead of external APIs, mocking:
  - `GET /assets?portfolioId={id}` → returns assets for portfolio
  - `GET /assets/{assetId}` → returns specific asset data
  - `POST /risk/analyze` → returns risk scores for asset list
  - `POST /investments/optimize` → returns optimization actions based on budget/horizon
- **UI**: Streamlit interface with LLM model selection, time horizon, and budget configuration
- **Authorization**: Mock service returning permissions based on user identity

### Security & Production Readiness
- **Authentication**: Future implementation with OIDC/Cognito for user identity
- **Authorization**: JWT claims/OAuth scopes for feature entitlement, IAM/DB row-level security for data access
- **Security Measures**:
  - Prevent prompt injection by never using user input in agent prompts
  - Feature-based access control at tool level
  - AWS Bedrock Guardrails for input/output validation
  - Mock database row-level security based on user

### Scalability Improvements
- **Managed Agent**: Move to AWS AgentCore for reusability as MCP server
- **Managed Tools**: Use AWS AgentCore Bedrock Gateway for cross-agent tool reuse
- **Long-Running Workflows**: Add persistent state management for multi-day operations
- **Enhanced Prompts**: More deterministic outputs with constrained response formats
- **Observability**: Comprehensive logging for explainability, security, and debugging
- **Operational Excellence**: IaC, Terraform 