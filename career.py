import streamlit as st
import pandas as pd
import google.generativeai as genai

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("profession_questions_answers.csv")

data = load_data()

# Configure Gemini API
API_KEY = "AIzaSyAYfcTAFba5mn5LXw4UNNfnBvQEgmNbAos"
genai.configure(api_key=API_KEY)

def get_gemini_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)
    return response.text if response else "I'm sorry, I couldn't generate a response."

# CSS for animated background and visible UI
st.markdown("""
<style>
@keyframes backgroundAnimation {
    0% { background-color: #FCE4EC; }
    20% { background-color: #E3F2FD; }
    40% { background-color: #E8F5E9; }
    60% { background-color: #FFFDE7; }
    80% { background-color: #F3E5F5; }
    100% { background-color: #E0F7FA; }
}

html, body {
    height: 100%;
    margin: 0;
    padding: 0;
}

.stApp {
    position: relative;
    z-index: 1;
    background: transparent !important;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: -1;
    animation: backgroundAnimation 10s infinite alternate;
}

/* Main content container */
.st-emotion-cache-1v0mbdj, .stMarkdown {
    position: relative;
    z-index: 2;
}

/* Input field styling */
.stTextInput>div>div>input {
    background: rgba(255,255,255,0.9) !important;
    border-radius: 20px !important;
    padding: 10px 15px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

/* Response container */
.response-box {
    background: rgba(255,255,255,0.9) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    margin: 20px 0 !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
}

/* Header and text visibility */
h1, h2, h3, p, .stMarkdown {
    color: #2c3e50 !important;
}

.center {
    display: flex;
    justify-content: center;
    z-index: 2;
    position: relative;
}
</style>
""", unsafe_allow_html=True)

# Centered GIF
st.markdown("""
<div class="center">
    <img src="https://cdn.pixabay.com/animation/2022/10/06/09/57/09-57-46-893_512.gif" width="200">
</div>
""", unsafe_allow_html=True)

# Chatbot Interface
st.title("🚀 Career Guidance Chatbot 🎯")
st.write("💡 Ask me any career-related questions!")

user_query = st.text_input("🔍 Type your question here:")

if user_query:
    # Check dataset first
    matched_row = data[data["Question"].str.lower() == user_query.lower()]
    
    if not matched_row.empty:
        answer = matched_row.iloc[0]["Answer"]
    else:
        # Get Gemini response if not in dataset
        answer = get_gemini_response(user_query)

    # Display response with styling
    st.markdown(f"""
    <div class="response-box">
        <h3>📝 Response:</h3>
        <p>{answer}</p>
    </div>
    """, unsafe_allow_html=True)
