# 🧭 TripAdvisor Chatbot

## 📌 Overview
An interactive **Streamlit chatbot** powered by **LangGraph**, **OpenAI**, and **Geoapify** APIs that helps users find **tourist attractions** in any city. Users can interact conversationally, customize search radius and result count, and view location details on the map.

---

## 🚀 Features

- 💬 Conversational chatbot UI with chat history.
- 📍 Location-aware responses using **Geoapify Places API**.
- 📌 Shows name, address, and map link for each attraction.
- 📐 Adjustable **search radius** and **number of attractions** via sidebar.
- ⚡️ Optimized with `st.cache_data()` to avoid redundant API calls.
- 🧠 Built using **LangGraph agentic workflow** powered by OpenAI.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: OpenAI GPT (via LangChain)
- **Workflow Engine**: LangGraph
- **APIs**: Geoapify (Geocoding + Places)

---

## 🛠️ Installation
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/Kushal2797/Trip_advisor_Agent.git
cd Trip_advisor_Agent
```

### 2️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Set Up API Key**
#### **Use a `.env` File (Recommended)**
1. Create a `.env` file in the same directory as the script.
2. Add your OpenAI API and GEOAPIFY key:
   ```
   OPENAI_API_KEY=your-api-key-here
   GEOAPIFY_API_KEY=your-api-key-here
   ```
3. The script will automatically read this key.

---

## 🚀 Usage
To run the CLI tool, use:
```bash
streamlit run app.py
```

---

## 📂 File Structure
```
tripadvisor-chatbot/
│
├── app.py                # Streamlit frontend + chat logic
├── agents.py             # LangGraph workflow nodes
├── tools.py              # API utilities for Geoapify
├── requirements.txt      # Dependencies
├── .env                  # API keys (not committed)
├── .gitignore            # Ignores .env, __pycache__, etc.
└── README.md             # You're here
```

---

## 🛠️ Assumptions &  Future Enhancements
### **Assumptions**
- User will only enter valid city name like "Ahmedabad", "Pune" etc.

### **Future Enhancements**
- Add filters by type (museums, parks, religious sites, etc.).
- Integrate real-time weather at location.
- Multilingual support
- Save favorite places
- Voice input for chat
---

## 📞 Contact
For support, please contact [kushalshah662@example.com](mailto:your-email@example.com).
