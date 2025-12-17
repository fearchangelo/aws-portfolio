import streamlit as st
from strands.models import BedrockModel
from agents import create_capital_planning_agent

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_budget" not in st.session_state:
    st.session_state.last_budget = None
if "last_horizon" not in st.session_state:
    st.session_state.last_horizon = None
if "last_user" not in st.session_state:
    st.session_state.last_user = None

# ============================================================================
# PAGE HEADER
# ============================================================================
st.title("Capital Planning AI Agentic System")
st.markdown("**Developed by Felipe Archangelo** | [💻 GitHub](https://github.com/fearchangelo) | [:briefcase: LinkedIn](https://linkedin.com/in/farchangelo)")
st.write("A Capital Planning AI Agentic System leveraging Amazon Bedrock LLMs and Guardrails to assist users in making informed capital planning decisions.")
st.write("Suggested questions:")
st.write("What assets are in portfolio p1?")
st.write("Perform a risk assessment on portfolio p1?")
st.write("Optimize portfolio p1.")

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================
with st.sidebar:
    st.header("Configuration")
    selected_user = st.selectbox(
        "User",
        ["User 1", "User 2"],
        index=0
    )
    selected_model = st.selectbox(
        "LLM Model",
        ["anthropic.claude-3-5-haiku-20241022-v1:0", "us.amazon.nova-lite-v1:0"],
        index=0
    )
    horizon_months = st.selectbox(
        "Horizon (months)",
        [6, 12, 18, 24, 30],
        index=1
    )
    budget = st.number_input(
        "Budget ($)",
        value=2000000,
        min_value=0,
        step=500000,
        format="%d"
    )

# ============================================================================
# AGENT INITIALIZATION
# ============================================================================

# In production, retrieve guardrail ID from parameter storage
model = BedrockModel(model_id=selected_model, 
                     max_tokens=4096,
                     guardrail_id="e9c8r9thmvgn",
                     guardrail_version="1",
                     guardrail_trace="enabled")

# Reinitialize agent if budget, horizon, or user changed
if (st.session_state.last_budget != budget or 
    st.session_state.last_horizon != horizon_months or
    st.session_state.last_user != selected_user):
    st.session_state.last_budget = budget
    st.session_state.last_horizon = horizon_months
    st.session_state.last_user = selected_user
    agent = create_capital_planning_agent(model, budget, horizon_months, selected_user)
    st.session_state.agent = agent
else:
    agent = st.session_state.get("agent", create_capital_planning_agent(model, budget, horizon_months, selected_user))
    st.session_state.agent = agent

# ============================================================================
# DISPLAY CHAT HISTORY
# ============================================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ============================================================================
# CHAT INPUT & RESPONSE
# ============================================================================
if user_input := st.chat_input("Ask me anything..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            agent_response = agent(user_input)
            response = str(agent_response)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()

# ============================================================================
# CLEAR CHAT BUTTON
# ============================================================================
if st.session_state.messages:
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
