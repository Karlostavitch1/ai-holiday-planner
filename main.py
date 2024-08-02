from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

from langchain_core.callbacks import BaseCallbackHandler
from crewai import Crew
from trip_agents import TripAgents
from trip_tasks import TripTasks
from typing import Any, Dict
import streamlit as st

# Initialize session state for messages, inputs, and authentication
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "location" not in st.session_state:
    st.session_state["location"] = ""

if "cities" not in st.session_state:
    st.session_state["cities"] = ""

if "date_range" not in st.session_state:
    st.session_state["date_range"] = ""

if "interests" not in st.session_state:
    st.session_state["interests"] = ""

if "processing" not in st.session_state:
    st.session_state["processing"] = False

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "plan_trip_clicked" not in st.session_state:
    st.session_state["plan_trip_clicked"] = False

# Define the password for authentication
PASSWORD = "DevPro2024!"

avatars = {
    "Writer": "https://cdn-icons-png.flaticon.com/512/320/320336.png",
    "Reviewer": "https://cdn-icons-png.freepik.com/512/9408/9408201.png"
}

class MyCustomHandler(BaseCallbackHandler):
    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Do nothing on chain start."""

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out the LLM response instead of the prompt."""
        response = outputs.get('output', 'No output available')
        st.session_state.messages.append({"role": self.agent_name, "content": response})
        st.chat_message(self.agent_name, avatar=avatars[self.agent_name]).write(response)

class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.date_range = date_range

    def run(self):
        handler = MyCustomHandler("TripPlanner")
        agents = TripAgents(callbacks=[handler])  # Pass the handler to TripAgents
        tasks = TripTasks()
        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        identify_task = tasks.identify_task(
            city_selector_agent,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )
        gather_task = tasks.gather_task(
            local_expert_agent,
            self.origin,
            self.interests,
            self.date_range
        )
        plan_task = tasks.plan_task(
            travel_concierge_agent, 
            self.origin,
            self.interests,
            self.date_range
        )

        crew = Crew(
            agents=[
                city_selector_agent, local_expert_agent, travel_concierge_agent
            ],
            tasks=[identify_task, gather_task, plan_task],
            verbose=True
        )

        result = crew.kickoff()
        return result

def login():
    st.title("🔒 Password Protected Web App")
    password = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if password == PASSWORD:
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid password")

if __name__ == "__main__":
    if st.session_state["authenticated"]:
        st.title("🌍 Trip Planner Crew")

        location = st.text_input("From where will you be traveling from?", value=st.session_state["location"])
        cities = st.text_input("What are the cities options you are interested in visiting?", value=st.session_state["cities"])
        date_range = st.text_input("What is the date range you are interested in traveling?", value=st.session_state["date_range"])
        interests = st.text_input("What are some of your high level interests and hobbies?", value=st.session_state["interests"])
        
        plan_trip_clicked = st.session_state.get("plan_trip_clicked", False)
        if st.button("Plan Trip", disabled=plan_trip_clicked or st.session_state["processing"]):
            if location and cities and date_range and interests:
                st.session_state["location"] = location
                st.session_state["cities"] = cities
                st.session_state["date_range"] = date_range
                st.session_state["interests"] = interests
                st.session_state["processing"] = True
                st.session_state["plan_trip_clicked"] = True
                with st.spinner("Planning your trip..."):
                    trip_crew = TripCrew(location, cities, date_range, interests)
                    result = trip_crew.run()
                st.session_state["processing"] = False
                st.session_state["plan_trip_clicked"] = False
                st.markdown("## Here is your Trip Plan")
                st.markdown(result)
            else:
                st.error("Please fill in all the fields.")
    else:
        login()
