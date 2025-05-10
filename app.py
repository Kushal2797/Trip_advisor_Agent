import streamlit as st
from agents import create_crew
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="TripAdvisor CrewAI Bot", page_icon="🌍")
st.title("TripAdvisor for Cities (CrewAI) 🤖")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

city_input = st.chat_input("Enter a city to explore:")

if city_input:
    st.session_state.chat_history.append(("user", city_input))
    with st.spinner("Assembling your travel crew..."):
        crew = create_crew(city_input)
        result = crew.run()
    st.session_state.chat_history.append(("bot", result))

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)
