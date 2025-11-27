import streamlit as st
from agents.nurse_agent_config import get_system_prompt
from agents.evaluator_agent_config import get_evaluator_prompt
from strands import Agent
from strands.models import BedrockModel
from tools.track_action import track_action, session

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "scenario_started" not in st.session_state:
    st.session_state.scenario_started = False
if "image_shown" not in st.session_state:
    st.session_state.image_shown = False

# ============================================================================
# PAGE HEADER
# ============================================================================
st.image("img/logo.webp", width=200)
st.title("BC Registered Nurse Assessment")
st.markdown("**Developed by Felipe Archangelo** | [💻 GitHub](https://github.com/fearchangelo) | [:briefcase: LinkedIn](https://linkedin.com/in/farchangelo)")
st.write("This application assesses your readiness to become a registered nurse 🏥 in British Columbia 🇨🇦 .")

# ============================================================================
# SCENARIO DEFINITION
# ============================================================================
SCENARIOS = {
    "Post-Operative Patient Care": {
        "name": "Post-Operative Patient Care",
        "description": "You are caring for a 65-year-old patient who just returned from surgery 2 hours ago. The patient is drowsy but responsive.",
        "necessary_actions": [
            "Check vital signs",
            "Review medication orders",
            "Assess level of consciousness"
        ],
        "red_flags": [
            "Administer medication without checking orders",
            "Skip vital signs assessment",
            "Leave patient unattended immediately",
            "Ignore pain complaints"
        ],
        "image": "img/scenario1.png"
    },
    "Emergency Room Triage": {
        "name": "Emergency Room Triage",
        "description": "A 45-year-old patient arrives at the ER complaining of severe chest pain radiating to the left arm. The patient is sweating profusely and appears anxious.",
        "necessary_actions": [
            "Check vital signs immediately",
            "Assess pain level and location",
            "Call for emergency assistance",
            "Prepare for ECG",
            "Keep patient calm and seated"
        ],
        "red_flags": [
            "Tell patient to wait in waiting room",
            "Dismiss symptoms as anxiety",
            "Leave patient alone",
            "Give medication without assessment"
        ],
        "image": "img/scenario2.png"
    }
}

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================
with st.sidebar:
    st.header("Configuration")
    selected_model = st.selectbox(
        "LLM",
        ["anthropic.claude-3-5-haiku-20241022-v1:0", "us.amazon.nova-lite-v1:0"],
        index=0
    )
    
    st.header("Scenario")
    selected_scenario_name = st.selectbox(
        "Select Scenario",
        list(SCENARIOS.keys()),
        index=0
    )

SCENARIO = SCENARIOS[selected_scenario_name]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def generate_final_report_prompt():
    return f"""
Scenario: {SCENARIO['name']}
{SCENARIO['description']}

Necessary Actions: {', '.join(SCENARIO['necessary_actions'])}
Completed Actions: {', '.join(session.completed_actions)}
Correct Actions: {', '.join(session.correct_actions)}
Red Flag Actions: {', '.join(session.red_flag_actions) if session.red_flag_actions else 'None'}

Provide a final assessment report.
"""

# ============================================================================
# AGENT INITIALIZATION
# ============================================================================
model = BedrockModel(model_id=selected_model, max_tokens=4096)

system_prompt = get_system_prompt(
    SCENARIO["name"],
    SCENARIO["description"],
    SCENARIO["necessary_actions"],
    SCENARIO["red_flags"]
)

agent = Agent(
    name="Nurse Evaluator",
    model=model,
    system_prompt=system_prompt,
    tools=[track_action],
)

evaluator_agent = Agent(
    name="Senior Evaluator",
    model=model,
    system_prompt=get_evaluator_prompt(),
    tools=[],
)

# ============================================================================
# START ASSESSMENT
# ============================================================================
if not st.session_state.scenario_started:
    if st.button("Start Assessment", use_container_width=True):
        st.session_state.scenario_started = True
        st.session_state.image_shown = True
        session.start_scenario(SCENARIO["name"])
        
        initial_response = agent("Present the scenario to the candidate and ask them what they would do first.")
        st.session_state.messages.append({"role": "assistant", "content": str(initial_response)})
        st.rerun()

# ============================================================================
# DISPLAY SCENARIO IMAGE
# ============================================================================
if st.session_state.scenario_started and st.session_state.image_shown:
    st.image(SCENARIO["image"], use_container_width=True)
    st.divider()

# ============================================================================
# DISPLAY CHAT HISTORY
# ============================================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ============================================================================
# CHAT INPUT & EVALUATION
# ============================================================================
if st.session_state.scenario_started:
    if user_input := st.chat_input("Describe your actions..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get agent evaluation
        with st.chat_message("assistant"):
            with st.spinner("Evaluating..."):
                agent_response = agent(f"The candidate said: '{user_input}'. Evaluate their response and guide them appropriately.")
                response = str(agent_response)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Check if assessment is complete
                if len(session.correct_actions) >= len(SCENARIO["necessary_actions"]):
                    evaluator_response = evaluator_agent(generate_final_report_prompt())
                    st.write("\n---\n")
                    st.write(str(evaluator_response))
                    st.session_state.messages.append({"role": "assistant", "content": str(evaluator_response)})
        
        st.rerun()

# ============================================================================
# RESET BUTTON
# ============================================================================
if st.session_state.scenario_started:
    if st.button("Reset Assessment", use_container_width=True):
        st.session_state.messages = []
        st.session_state.scenario_started = False
        st.session_state.image_shown = False
        session.reset()
        st.rerun()

# ============================================================================
# PROGRESS SIDEBAR
# ============================================================================
if st.session_state.scenario_started:
    with st.sidebar:
        st.header("Progress")
        st.write(f"**Completed Actions: ({len(session.correct_actions)}/{len(SCENARIO['necessary_actions'])})**")
        for action in SCENARIO['necessary_actions']:
            if action in session.correct_actions:
                st.markdown(f"✅ {action}")
        
        if session.red_flag_actions:
            st.warning(f"**Red Flags:** {len(session.red_flag_actions)}")
