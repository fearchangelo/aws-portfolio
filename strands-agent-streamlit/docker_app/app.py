import streamlit as st
import json
import boto3

from strands import Agent
from strands.models import BedrockModel
from tools.suggest_travel_destination import suggest_travel_destination, session as suggest_session
from tools.pick_travel_destination import pick_travel_destination, session as pick_session

# Use the same session instance
session = suggest_session
from agents.agent_config import system_prompt

def get_flag_emoji(city):
    """Get flag emoji for a city using known mappings or LLM"""
    city_flags = {
        "vancouver": "🇨🇦", "toronto": "🇨🇦", "montreal": "🇨🇦",
        "berlin": "🇩🇪", "munich": "🇩🇪", "hamburg": "🇩🇪",
        "sao paulo": "🇧🇷", "rio de janeiro": "🇧🇷", "brasilia": "🇧🇷",
        "new york": "🇺🇸", "los angeles": "🇺🇸", "chicago": "🇺🇸",
        "london": "🇬🇧", "manchester": "🇬🇧", "birmingham": "🇬🇧",
        "paris": "🇫🇷", "lyon": "🇫🇷", "marseille": "🇫🇷",
        "tokyo": "🇯🇵", "osaka": "🇯🇵", "kyoto": "🇯🇵"
    }
    
    flag = city_flags.get(city.lower())
    if flag:
        return flag
    
    # Use LLM for unknown cities
    try:
        bedrock = boto3.client('bedrock-runtime')
        prompt = f"What is the flag emoji for the country where {city} is located? Return only the flag emoji, no text."
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 5,
            "messages": [{"role": "user", "content": prompt}]
        })
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-5-haiku-20241022-v1:0",
            body=body
        )
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text'].strip() or "🏳️"
    except:
        return "🏳️"

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "output" not in st.session_state:
    st.session_state.output = []
if "details_placeholder" not in st.session_state:
    st.session_state.details_placeholder = None

st.title("Travel Destination Picker powered by Agentic AI")
st.write("This app helps a group decide on a travel destination using Agentic AI.")

if ("participants" not in st.session_state):
    st.session_state.participants = [
    {"name": "Phillip", "city": "Vancouver", "personality": "enjoys hikes, beach, dogs"},
    {"name": "Bruno", "city": "Berlin", "personality": "enjoys bbq, beer, sports"},
    {"name": "Rafael", "city": "Sao Paulo", "personality": "enjoys sports, running"}]

# Sidebar for participant management
with st.sidebar:
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

# Display chat history
if not st.session_state.messages:
    st.markdown("### How it works:")
    st.markdown("PHASE 1. **Participants** suggest travel destinations based on their city and personality")
    st.markdown("PHASE 2. **Participants** pick a travel destination from all other proposals")
    st.markdown("FINAL RESULT: The most popular travel destination is selected")
    st.markdown("\n*Try asking: 'Where should we travel for a week at the beach?'*")

# Define LLM
model = BedrockModel(
    model_id="anthropic.claude-3-5-haiku-20241022-v1:0",
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

# Keep track of the number of previous messages in the agent flow
if "start_index" not in st.session_state:
    st.session_state.start_index = 0

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.empty()  # This forces the container to render without adding visible content (workaround for streamlit bug)
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your agent..."):
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
                agent(prompt)

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

                print(f"DEBUG: Agent {agent.name} session data: {session.data[agent.name]}")

                chosen = session.data[agent.name]['suggested_travel_location']
                reason = session.data[agent.name]['suggestion_reasoning']

                choices_text = f"• {agent.name} picked {chosen}, arguing '{reason}'.  \n"
            
                st.write(choices_text)
                st.session_state.messages.append({"role": "assistant", "content": choices_text})

        with st.spinner("FINAL RESULT!"):
            st.write("\n**Final Result:**\n\n")
        
            most_common = session.get_most_chosen()
            if most_common:
                result_text = f"{most_common} is the most popular choice!"
                st.write(result_text)
                st.session_state.messages.append({"role": "assistant", "content": result_text})

