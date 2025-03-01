import streamlit as st
import pandas as pd
import google.generativeai as genai

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("profession_questions_answers.csv")

data = load_data()

# Directly embedding the Gemini API Key
API_KEY = "AIzaSyAYfcTAFba5mn5LXw4UNNfnBvQEgmNbAos"  # Replace with your actual Gemini API Key
genai.configure(api_key=API_KEY)

def get_gemini_response(user_input):
    """Function to get response from the Gemini API"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)
    return response.text if response else "I'm sorry, I couldn't generate a response."

# More gradient colors for dynamic background
gradient_colors = [
    "#FFDEE9, #B5FFFC", "#A1C4FD, #C2E9FB", "#FFEFBA, #FFFFFF", "#FAACA8, #DDD6F3",
    "#FAD961, #F76B1C", "#FDCB82, #FF9A8B", "#A18CD1, #FBC2EB", "#F7CE68, #FBAB7E",
    "#70F570, #49C628", "#30Cfd0, #330867", "#667eea, #764ba2", "#FF9A9E, #FAD0C4"
]

# Inject CSS for animated background & chat styling
st.markdown(
    f"""
    <style>
    @keyframes gradientChange {{
        0%   {{ background: linear-gradient(135deg, {gradient_colors[0]}); }}
        8%   {{ background: linear-gradient(135deg, {gradient_colors[1]}); }}
        16%  {{ background: linear-gradient(135deg, {gradient_colors[2]}); }}
        25%  {{ background: linear-gradient(135deg, {gradient_colors[3]}); }}
        33%  {{ background: linear-gradient(135deg, {gradient_colors[4]}); }}
        41%  {{ background: linear-gradient(135deg, {gradient_colors[5]}); }}
        50%  {{ background: linear-gradient(135deg, {gradient_colors[6]}); }}
        58%  {{ background: linear-gradient(135deg, {gradient_colors[7]}); }}
        66%  {{ background: linear-gradient(135deg, {gradient_colors[8]}); }}
        75%  {{ background: linear-gradient(135deg, {gradient_colors[9]}); }}
        83%  {{ background: linear-gradient(135deg, {gradient_colors[10]}); }}
        91%  {{ background: linear-gradient(135deg, {gradient_colors[11]}); }}
        100% {{ background: linear-gradient(135deg, {gradient_colors[0]}); }}
    }}
    .stApp {{
        animation: gradientChange 15s infinite alternate;
        background-size: cover;
    }}

    /* Chat bubbles */
    .bot-message {{
        background-color: #f0f0f5;
        color: #333;
        padding: 10px 15px;
        border-radius: 15px;
        width: fit-content;
        max-width: 70%;
        margin: 10px 0;
        text-align: left;
        font-family: Arial, sans-serif;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }}

    .user-message {{
        background-color: #0078ff;
        color: white;
        padding: 10px 15px;
        border-radius: 15px;
        width: fit-content;
        max-width: 70%;
        margin: 10px 0 10px auto;
        text-align: right;
        font-family: Arial, sans-serif;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
    }}

    /* Input box styling */
    .stTextInput > div > div {{
        border-radius: 25px;
        padding: 10px;
        border: 2px solid #0078ff;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Display the animated GIF properly
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.pinimg.com/originals/1f/f3/3e/1ff33ede4825194fdbcf0f9b5e27dc93.gif" width="250" height="150">
    </div>
    """,
    unsafe_allow_html=True
)

# Chatbot UI
st.title("🚀 Career Guidance Chatbot 🎯")
st.write("Ask me career-related questions!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages with proper alignment
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["text"]}</div>', unsafe_allow_html=True)

# User Input Box at the Bottom
user_query = st.text_input("Type your message and press Enter", key="user_input")

if user_query:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "text": user_query})

    # Check if the question exists in the dataset
    matched_row = data[data["Question"].str.lower() == user_query.lower()]
    
    if not matched_row.empty:
        answer = matched_row.iloc[0]["Answer"]
    else:
        answer = get_gemini_response(user_query)

    # Add bot response to session state
    st.session_state.messages.append({"role": "bot", "text": answer})

    # Refresh page to show new messages
    st.text_input("Type your message and press Enter", key="user_input", value="", on_change=None)

