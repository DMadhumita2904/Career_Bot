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

# CSS for background color animation
st.markdown(
    """
    <style>
    @keyframes backgroundAnimation {
        0% {background-color: #FCE4EC;}
        20% {background-color: #E3F2FD;}
        40% {background-color: #E8F5E9;}
        60% {background-color: #FFFDE7;}
        80% {background-color: #F3E5F5;}
        100% {background-color: #E0F7FA;}
    }
    
    html, body, [class*="css"] {
        min-height: 100vh;
    }
    
    .stApp {
        animation: backgroundAnimation 10s infinite alternate !important;
        background: transparent !important;
    }
    
    .stApp > header {
        background-color: transparent !important;
    }
    
    .stApp > div {
        background-color: transparent !important;
    }
    
    /* Force text elements to maintain visibility */
    .stMarkdown, .stTextInput, .stButton > button, .stAlert {
        color: #333333 !important;
        background: transparent !important;
    }
    
    .center {
        display: flex;
        justify-content: center;
        background: transparent !important;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.9) !important;
        border-radius: 20px !important;
        padding: 10px 15px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centered GIF with reduced size
st.markdown(
    """
    <div class="center">
        <img src="https://cdn.pixabay.com/animation/2022/10/06/09/57/09-57-46-893_512.gif" width="200">
    </div>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("🚀 Career Guidance Chatbot 🎯")
st.write("💡 Ask me any career-related questions!")

# User Input
user_query = st.text_input("🔍 Type your question here:")

if user_query:
    # Check if the question exists in the dataset
    matched_row = data[data["Question"].str.lower() == user_query.lower()]
    
    if not matched_row.empty:
        answer = matched_row.iloc[0]["Answer"]
    else:
        answer = get_gemini_response(user_query)

    # Response container with styling
    st.markdown(
        f'<div style="background: rgba(255,255,255,0.9); '
        f'padding: 20px; border-radius: 15px; margin: 20px 0;">'
        f'<h3 style="color: #2c3e50;">📝 Response:</h3>'
        f'<p style="color: #34495e;">{answer}</p></div>',
        unsafe_allow_html=True
    )
