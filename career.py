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

# Callback function to clear input field
def clear_input():
    st.session_state["user_input"] = ""

# Chatbot UI
st.title("🚀 Career Guidance Chatbot 🎯")
st.write("Ask me career-related questions!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["text"]}</div>', unsafe_allow_html=True)

# Use a text input with an on-change callback to clear input
user_query = st.text_input("Type your message and press Enter", key="user_input", on_change=clear_input)

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

    # Force rerun to display messages
    st.rerun()
