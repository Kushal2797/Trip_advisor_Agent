import streamlit as st
from agents import build_graph

graph = build_graph()

st.title("🧭 TripAdvisor Chatbot")

city = st.text_input("Enter a city name")

if st.button("Find Tourist Attractions"):
    if not city.strip():
        st.error("Please enter a city name.")
    else:
        with st.spinner("Fetching info..."):
            st.write(f"Invoking graph with city: {city}")
            result = graph.invoke({"city": city})
            spots = result.get("spots", [])
            if not spots:
                st.warning(f"No tourist spots found for {city}.")
            else:
                st.success(f"Top spots in {city}:")
                for spot in spots:
                    st.write("• " + spot)
