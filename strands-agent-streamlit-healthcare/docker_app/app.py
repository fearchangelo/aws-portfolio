import streamlit as st
from agents.nurse_agent_config import get_system_prompt
from agents.evaluator_agent_config import get_evaluator_prompt
from strands import Agent
from strands.models import BedrockModel
from tools.track_action import track_action, session

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "scenario_started" not in st.session_state:
    st.session_state.scenario_started = False
if "image_shown" not in st.session_state:
    st.session_state.image_shown = False

st.image("img/logo.webp", width=200)
st.title("BC Registered Nurse Assessment")
st.markdown("**Developed by Felipe Archangelo** | [💻 GitHub](https://github.com/fearchangelo) | [:briefcase: LinkedIn](https://linkedin.com/in/farchangelo)")
st.write("This application assesses your readiness to become a registered nurse 🏥 in British Columbia 🇨🇦.")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    selected_model = st.selectbox(
        "LLM",
        ["anthropic.claude-3-5-haiku-20241022-v1:0", "us.amazon.nova-lite-v1:0"],
        index=0
    )
    
    st.header("Scenario")
    scenario_name = "Patient Care Scenario #1"
    st.write(f"**Current:** {scenario_name}")

# Define scenario
SCENARIO = {
    "name": "Patient Care Scenario #1",
    "description": "You enter a patient's room and find a 72-year-old woman who reports: *I'm dizzy and my chest hurts.* Her skin looks pale, and she is breathing faster than normal.",
    "necessary_actions": [
        "Check vital signs",
        "Make the patient comfortable",
        "Call for help"
    ],
    "red_flags": [
        "Leave patient alone",
        "Say it's just anxiety",
        "Give medication without assessment",
        "Perform any kind of procedure without proper authorization"
    ]
}

# Initialize model and agent
model = BedrockModel(
    model_id=selected_model,
    max_tokens=4096,
)

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

# Start scenario button
if not st.session_state.scenario_started:
    if st.button("Start Assessment", use_container_width=True):
        st.session_state.scenario_started = True
        session.start_scenario(SCENARIO["name"])
        st.session_state.image_shown = True
        
        # Agent presents scenario
        initial_response = agent(f"Present the scenario to the candidate and ask them what they would do first.")
        initial_message = str(initial_response)
        st.session_state.messages.append({"role": "assistant", "content": initial_message})
        st.rerun()

# Display scenario image once at the beginning (outside chat container)
if st.session_state.scenario_started and st.session_state.image_shown:
    st.image("img/scenario1.jpg", use_container_width=True)
    st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if st.session_state.scenario_started:
    if user_input := st.chat_input("Describe your actions..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Evaluating..."):
                # Continue assessment with first agent
                agent_response = agent(f"The candidate said: '{user_input}'. Evaluate their response and guide them appropriately.")
                response = str(agent_response)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Check if all necessary actions completed after agent response
                if len(session.correct_actions) >= len(SCENARIO["necessary_actions"]):
                    # Generate final report using evaluator agent
                    report_prompt = f"""
Scenario: {SCENARIO['name']}
{SCENARIO['description']}

Necessary Actions: {', '.join(SCENARIO['necessary_actions'])}

Completed Actions: {', '.join(session.completed_actions)}

Correct Actions: {', '.join(session.correct_actions)}

Red Flag Actions: {', '.join(session.red_flag_actions) if session.red_flag_actions else 'None'}

Provide a final assessment report.
"""
                    evaluator_response = evaluator_agent(report_prompt)
                    final_report = str(evaluator_response)
                    st.write("\n---\n")
                    st.write(final_report)
                    st.session_state.messages.append({"role": "assistant", "content": final_report})
        
        st.rerun()

# Reset button at bottom
if st.session_state.scenario_started:
    if st.button("Reset Assessment", use_container_width=True):
        st.session_state.messages = []
        st.session_state.scenario_started = False
        st.session_state.image_shown = False
        session.reset()
        st.rerun()

# Progress indicator
if st.session_state.scenario_started:
    with st.sidebar:
        st.header("Progress")
        st.write("**Completed Actions:**")
        for action in SCENARIO['necessary_actions']:
            if action in session.correct_actions:
                st.markdown(f"✅ {action}")
        
        if session.red_flag_actions:
            st.warning(f"**Red Flags:** {len(session.red_flag_actions)}")
