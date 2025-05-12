import streamlit as st
from agents import build_graph

graph = build_graph()
st.set_page_config(page_title="TripAdvisor Bot", page_icon="🧭", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #0077b6;'>🧭 TripAdvisor Travel Assistant</h1>", 
    unsafe_allow_html=True
)
st.markdown("Get tourist attraction recommendations for your favorite city 🌆.")

with st.sidebar:
    st.markdown("### 🔍 How it works")
    st.write("Enter a city to discover its top tourist attractions using AI & Geoapify!")
    radius = st.sidebar.slider("Search Radius (meters)", 500, 5000, 1000)
    limit = st.sidebar.slider("Number of Attractions", 5, 30, 10)

# Session state for history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render history
for msg in st.session_state.messages:
    st.chat_message("user").write(msg["user"])
    st.chat_message("bot").markdown(msg["bot"], unsafe_allow_html=True)

# New user input
prompt = st.chat_input("Enter a city name to explore...")

if prompt:
    st.chat_message("user").write(prompt)
    result = graph.invoke({"city": prompt, "radius": radius, "limit": limit})
    

    # Handle error if city is invalid
    if "error" in result:
        reply = result["error"]
        st.chat_message("bot").error(reply)
    else:
        spots = result.get("spots", [])
        
        if not spots:
            reply = "😕 I couldn't find tourist spots in this city. Please make sure the city name is valid or try another city."
        else:
            reply = f"### 🗺️ Top tourist spots in **{prompt}**:\n"
            for spot in spots:
                
                name = spot.get("name", "No name available")
                if name != "Unknown place":
                    address = spot.get("address", "Address not available")
                    # spot_type = spot.get("type", "Type not specified")
                    coords = spot.get("coords", [0, 0])
                    lat, lon = coords
                    map_link = f"[View on Map](https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon})"

                    reply += f"- ✅ **{name}**\n"
                    # reply += f"  - 🏷️ **Type**: {spot_type}\n"
                    reply += f"  - 🏠 **Address**: {address}\n"
                    reply += f"  - 🗺️ {map_link}\n\n"

        st.chat_message("bot").markdown(reply, unsafe_allow_html=True)

    # Append user-bot conversation to session state for history
    st.session_state.messages.append({"user": prompt, "bot": reply})



