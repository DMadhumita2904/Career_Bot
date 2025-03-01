import streamlit as st
import pandas as pd
import google.generativeai as genai

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("profession_questions_answers.csv")

data = load_data()

# API Key Configuration
API_KEY = "AIzaSyAYfcTAFba5mn5LXw4UNNfnBvQEgmNbAos"  # Replace with your actual Gemini API Key
genai.configure(api_key=API_KEY)

def get_gemini_response(user_input):
    """Function to get response from Gemini API"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)
    return response.text if response else "I'm sorry, I couldn't generate a response."

# Dynamic background gradient
gradient_colors = [
    "#FFDEE9, #B5FFFC", "#A1C4FD, #C2E9FB", "#FFEFBA, #FFFFFF",
    "#FAACA8, #DDD6F3", "#FAD961, #F76B1C", "#FDCB82, #FF9A8B",
    "#A18CD1, #FBC2EB", "#F7CE68, #FBAB7E", "#70F570, #49C628",
    "#30Cfd0, #330867", "#667eea, #764ba2", "#FF9A9E, #FAD0C4"
]

# Inject CSS for animated background and chat bubble styling
st.markdown(
    f"""
    <style>
    @keyframes gradientChange {{
        0%   {{ background: linear-gradient(135deg, {gradient_colors[0]}); }}
        100% {{ background: linear-gradient(135deg, {gradient_colors[-1]}); }}
    }}
    .stApp {{ animation: gradientChange 15s infinite alternate; background-size: cover; }}
    
    .chat-container {{
        max-height: 400px; overflow-y: auto; padding: 10px;
        border-radius: 10px; background: rgba(255, 255, 255, 0.2);
    }}

    .bot-message {{
        background-color: #f0f0f5; color: #333; padding: 10px 15px;
        border-radius: 10px; max-width: 70%;
        margin: 10px 0; text-align: left; font-family: Arial, sans-serif;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }}

    .user-message {{
        background-color: #0078ff; color: white; padding: 10px 15px;
        border-radius: 10px; max-width: 70%;
        margin: 10px 0 10px auto; text-align: right; font-family: Arial, sans-serif;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
    }}

    .chat-input {{
        position: fixed; bottom: 20px; width: 90%;
        background: white; padding: 10px;
        border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Display GIF at the top
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.pinimg.com/originals/1f/f3/3e/1ff33ede4825194fdbcf0f9b5e27dc93.gif" width="300" height="200">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🚀 Career Guidance Chatbot 🎯")
st.write("Ask me career-related questions!")

# Initialize chat session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history inside a scrollable container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["text"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# User input at the bottom
user_query = st.text_input("Type your question here and press Enter:", key="user_input")

if user_query.strip():
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "text": user_query})

    # Check if question exists in dataset
    matched_row = data[data["Question"].str.lower() == user_query.lower()]
    
    if not matched_row.empty:
        answer = matched_row.iloc[0]["Answer"]
    else:
        answer = get_gemini_response(user_query)

    # Add bot response to session state
    st.session_state.messages.append({"role": "bot", "text": answer})

    # Clear input and refresh chat
    st.session_state["user_input"] = ""
    st.experimental_rerun()
