import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Load the dataset with caching
@st.cache_data
def load_data():
    return pd.read_csv("profession_questions_answers.csv")

df = load_data()

def get_predefined_answer(profession, question):
    """Fetch the predefined answer from the dataset."""
    row = df[(df["Profession"] == profession) & (df["Question"] == question)]
    return row["Answer"].values[0] if not row.empty else None

# Set up Gemini API
GEMINI_API_KEY = os.getenv("AIzaSyAYfcTAFba5mn5LXw4UNNfnBvQEgmNbAos")  # Set your API key in environment variables
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(question):
    """Fetch additional insights from Gemini AI using Gemini Flash 1.5."""
    model = genai.GenerativeModel("gemini-flash-1.5")
    response = model.generate_content(question)
    return response.text if response else "I'm unable to fetch additional details at the moment."

# Streamlit UI with enhanced design
st.set_page_config(page_title="Career Guidance Chatbot", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    .main {background-color: #f4f4f4;}
    .stTextInput, .stSelectbox {border-radius: 10px;}
    .stButton button {background-color: #4CAF50; color: white; font-size: 18px; padding: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Career Guidance Chatbot")
st.caption("Get expert insights and guidance for your career path.")

st.markdown("""
    ### 🔍 How It Works:
    1. Select a profession from the dropdown.
    2. Choose a career-related question.
    3. Get expert advice and AI-powered insights!
""")

# User input
profession = st.selectbox("🔹 Choose a profession:", df["Profession"].unique())
question = st.selectbox("🔹 Choose a question:", df[df["Profession"] == profession]["Question"].unique())

if st.button("✨ Get Answer ✨"):
    predefined_answer = get_predefined_answer(profession, question)
    gemini_answer = get_gemini_response(question)
    
    st.subheader("📌 Predefined Answer:")
    st.write(predefined_answer)
    
    st.subheader("🤖 Additional Insights from Gemini AI:")
    st.write(gemini_answer)

st.markdown("""
    ---
    **💡 Pro Tip:** Keep exploring different professions and questions to find your perfect career path!
""")

# To run this Streamlit app, use:
# streamlit run app.py
