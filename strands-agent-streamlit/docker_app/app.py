import streamlit as st
import json
import boto3

from agents.agent_config import system_prompt
from strands import Agent
from strands.models import BedrockModel
from tools.suggest_travel_destination import suggest_travel_destination, session as suggest_session
from tools.pick_travel_destination import pick_travel_destination, session as pick_session

from time import sleep

# Use the same session instance
session = suggest_session

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Travel Destination Picker")
st.write("This app helps a group decide on a travel destination using Agentic AI.")
st.write("Use the sidebar to add or remove participants with their city and personality.")
st.write("You can also configure the LLM powering the decision-making process.")

if ("participants" not in st.session_state):
    st.session_state.participants = [
    {"name": "Julian", "city": "Portland", "personality": "likes edm music, nightlife, cocktails"},
    {"name": "Kevin", "city": "San Francisco", "personality": "tech junkie, likes taking photographs, craft beer"},
    {"name": "Josh", "city": "Vancouver", "personality": "likes dogs, hiking, beach, coffee, doesnt drink alcohol"}]

# Sidebar for participant management
with st.sidebar:
    st.header("Configuration")
    
    # Model selection
    selected_model = st.selectbox(
        "LLM",
        ["anthropic.claude-3-5-haiku-20241022-v1:0", "us.amazon.nova-lite-v1:0"],
        index=0
    )
    
    st.header("Participants")
    
    # Add new participant
    with st.expander("Add Participant"):
        new_name = st.text_input("Name")
        new_city = st.text_input("City", placeholder="e.g. Toronto")
        new_personality = st.text_area("Personality", placeholder="e.g. loves adventure, prefers luxury, etc")
        
        if st.button("Add") and new_name and new_city:
            st.session_state.participants.append({
                "name": new_name,
                "city": new_city,
                "personality": new_personality
            })
            st.rerun()
    
    # Display and manage existing participants
    for i, p in enumerate(st.session_state.participants):
        with st.expander(f"{p['name']}"):
            st.write(f"**City:** {p['city']}")
            st.write(f"**Personality:** {p['personality']}")
            if st.button(f"Remove {p['name']}", key=f"remove_{i}"):
                st.session_state.participants.pop(i)
                st.rerun()

# Participant group buttons
st.markdown("### Participant Groups:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Phil 🇨🇦, Bruno 🇩🇪, Renny 🇧🇷", use_container_width=True):
        st.session_state.participants = [
            {"name": "Phil", "city": "Vancouver", "personality": "enjoys hikes, beach, dogs"},
            {"name": "Bruno", "city": "Berlin", "personality": "enjoys bbq, beer, sports"},
            {"name": "Renny", "city": "Sao Paulo", "personality": "enjoys beer, formula one, workaholic"}
        ]
        st.rerun()

with col2:
    if st.button("Jess 🇨🇦, Natalie 🇬🇧, Trish 🇺🇸", use_container_width=True):
        st.session_state.participants = [
            {"name": "Jess", "city": "Vancouver", "personality": "enjoys dogs, beach, shopping"},
            {"name": "Natalie", "city": "London", "personality": "enjoys books, coffee, history"},
            {"name": "Trish", "city": "Washington DC", "personality": "enjoys skiing, mountain"}
        ]
        st.rerun()

with col3:
    if st.button("Julian 🇺🇸, Kevin 🇺🇸, Josh 🇨🇦", use_container_width=True):
        st.session_state.participants = [
            {"name": "Julian", "city": "Portland", "personality": "likes edm music, nightlife, cocktails"},
            {"name": "Kevin", "city": "San Francisco", "personality": "tech junkie, likes taking photographs, craft beer"},
            {"name": "Josh", "city": "Vancouver", "personality": "likes dogs, hiking, beach, coffee, doesnt drink alcohol"}
        ]
        st.rerun()

# Quick prompt buttons
st.markdown("### Quick Travel Ideas:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏖️ Beach Retreat", use_container_width=True):
        st.session_state.selected_prompt = "Where should we travel for a week at the beach?"

with col2:
    if st.button("❄️ Winter Village", use_container_width=True):
        st.session_state.selected_prompt = "Where should we travel for a weekend in a cozy winter village?"

with col3:
    if st.button("👨‍👩‍👧‍👦 Family Trip", use_container_width=True):
        st.session_state.selected_prompt = "Where should we travel for vacation with kids?"

with col4:
    if st.button("🛍️ Luxury Shopping", use_container_width=True):
        st.session_state.selected_prompt = "Where should we travel for luxury shopping?"

# Define LLM
model = BedrockModel(
    model_id=selected_model,
    max_tokens=8192,
)

# Create agents for each participant
agents = []
for participant in st.session_state.participants:
    participant_prompt = system_prompt + f"\n\nYour name is {participant['name']}, you live in {participant['city']}, and your personality: {participant['personality']}."
    agent = Agent(
        name=participant['name'],
        model=model,
        system_prompt=participant_prompt,
        tools=[suggest_travel_destination, pick_travel_destination],
    )
    agents.append(agent)

# State to track process completion
if "process_completed" not in st.session_state:
    st.session_state.process_completed = False

# Handle selected prompt from buttons
if "selected_prompt" in st.session_state:
    prompt = st.session_state.selected_prompt
    del st.session_state.selected_prompt
else:
    prompt = None

# Reset button (always visible)
if st.button("Reset", use_container_width=True):
    st.session_state.messages = []
    st.session_state.process_completed = False
    st.rerun()

# Handle prompt
if prompt and not st.session_state.process_completed:
    #
    st.session_state.messages = []
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Execute agent output
    with st.chat_message("assistant"):
        # Clear previous session data and output
        session.data.clear()
        st.session_state.output = []
        st.session_state.details_placeholder = st.empty()

        with st.spinner("PHASE 1: Agents are suggesting travel locations..."):
            st.write("**Travel Proposals:**\n\n")
            
            for agent in agents:
                already_suggested = session.get_all_suggestions()
                agent(f"{prompt} Use the suggest_travel_destination tool with already_suggested: {already_suggested}")

                destination = session.data[agent.name]['suggested_travel_location']
                reasoning = session.data[agent.name].get('suggestion_reasoning', '')
                proposals_text = f"• {agent.name} proposed {destination} arguing '{reasoning}'.  \n"

                st.write(proposals_text)
                st.session_state.messages.append({"role": "assistant", "content": proposals_text})

        with st.spinner("PHASE 2: Agents are picking travel destinations..."):
            st.write("\n**Travel Choices:**\n\n")
            
            for agent in agents:
                other_destinations = session.get_other_destinations(agent.name)
                agent(f"Pick your preferred destination from these options: {other_destinations}. Use the pick_travel_destination tool.")

                if 'chosen_destination' in session.data[agent.name] and 'reason' in session.data[agent.name]:
                    chosen = session.data[agent.name]['chosen_destination']
                    reason = session.data[agent.name]['reason']
                else:
                    continue

                choices_text = f"• {agent.name} picked {chosen}, arguing '{reason}'.  \n"

                st.write(choices_text)
                st.session_state.messages.append({"role": "assistant", "content": choices_text})

        with st.spinner("FINAL RESULT!"):
            st.write("\n**Final Result:**\n\n")
        
            most_common = session.get_most_chosen()
            if most_common:
                result_text = f"🌍✨🎉 {most_common} has been chosen as the travel destination for the group! 🎉✨🌍"
                st.write(result_text)
                st.session_state.messages.append({"role": "assistant", "content": result_text})


