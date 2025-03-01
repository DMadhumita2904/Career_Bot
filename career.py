import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
import random

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

# List of light colors for background
light_colors = ["#FCE4EC", "#E3F2FD", "#E8F5E9", "#FFFDE7", "#F3E5F5", "#E0F7FA", "#FFEBEE"]

# Streamlit UI - Background Color Changer
def set_background():
    """Dynamically change background color every few seconds."""
    color = random.choice(light_colors)
    st.markdown(
        f"""
        <style>
        body {{
            background-color: {color};
            transition: background-color 1s ease;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background()

# UI Design
st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        color: #673AB7;
    }
    .subtext {
        font-size: 18px;
        text-align: center;
        color: #424242;
        font-style: italic;
    }
    .chatbox {
        border: 2px solid #673AB7;
        border-radius: 10px;
        padding: 15px;
        background-color: #FFFFFF;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Adding a GIF image at the top
st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Ftenor.com%2Fsearch%2Fcareer-jobs-gifs&psig=AOvVaw0CyEK9iUBcv_x5tDyHpJ40&ust=1740894606883000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCPig7feX6IsDFQAAAAAdAAAAABAo", use_container_width=True)

st.markdown('<p class="main-title">Career Guidance Chatbot 🎯</p>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Your personal AI career advisor 🤖</p>', unsafe_allow_html=True)

# User Input Section
st.markdown('<div class="chatbox">', unsafe_allow_html=True)
user_query = st.text_input("Type your question here:")

if user_query:
    matched_row = data[data["Question"].str.lower() == user_query.lower()]
    
    if not matched_row.empty:
        answer = matched_row.iloc[0]["Answer"]
    else:
        answer = get_gemini_response(user_query)

    st.write("### Response:")
    st.write(answer)

st.markdown('</div>', unsafe_allow_html=True)



