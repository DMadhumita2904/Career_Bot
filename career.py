import streamlit as st
import pandas as pd
import google.generativeai as genai

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("profession_questions_answers.csv")

data = load_data()

# Directly embedding the Gemini API Key
API_KEY = "AIzaSyAYfcTAFba5mn5LXw4UNNfnBvQEgmNbAos"
genai.configure(api_key=API_KEY)

def get_gemini_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)
    return response.text if response else "I'm sorry, I couldn't generate a response."

# CSS for background color animation (final working version)
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
    width: 100%;
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
    background-color: #FCE4EC;
}

.stApp > div,
.stApp > header,
.stMarkdown,
.stTextInput,
.stButton > button {
    background: transparent !important;
}

.stTextInput>div>div>input {
    background: rgba(255,255,255,0.9) !important;
    border-radius: 20px !important;
    padding: 10px 15px !important;
}

.stMarkdown div[data-testid="stMarkdownContainer"] {
    background: rgba(255,255,255,0.9) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    margin: 20px 0 !important;
}

.center {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# Centered GIF
st.markdown("""
<div class="center">
    <img src="https://cdn.pixabay.com/animation/2022/10/06/09/57/09-57-46-893_512.gif" width="200">
</div>
""", unsafe_allow_html=True)

# UI Components
st.title("🚀 Career Guidance Chatbot 🎯")
st.write("💡 Ask me any career-related questions!")

user_query = st.text_input("🔍 Type your question here:")

if user_query:
    matched_row = data[data["Question"].str.lower() == user_query.lower()]
    answer = matched_row.iloc[0]["Answer"] if not matched_row.empty else get_gemini_response(user_query)
    st.markdown(f"""
    <div style="color: #2c3e50;">
        <h3>📝 Response:</h3>
        <p style="color: #34495e;">{answer}</p>
    </div>
    """, unsafe_allow_html=True)
