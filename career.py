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
    "#FFDEE9, #B5FFFC",  # Light pink to blue
    "#A1C4FD, #C2E9FB",  # Soft blue to white
    "#FFEFBA, #FFFFFF",  # Light yellow to white
    "#FAACA8, #DDD6F3",  # Soft red to purple
    "#FAD961, #F76B1C",  # Orange gradient
    "#FDCB82, #FF9A8B",  # Peach to soft pink
    "#A18CD1, #FBC2EB",  # Purple to pink
    "#F7CE68, #FBAB7E",  # Gold to soft orange
    "#70F570, #49C628",  # Bright green to deep green
    "#30Cfd0, #330867",  # Turquoise to deep blue
    "#667eea, #764ba2",  # Blue to purple
    "#FF9A9E, #FAD0C4",  # Soft red to peach
]

# Inject CSS for animated gradient background
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
        animation: gradientChange 5s infinite alternate;
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Display the animated GIF properly
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.pinimg.com/originals/1f/f3/3e/1ff33ede4825194fdbcf0f9b5e27dc93.gif" width="300" height="300">
    </div>
    """,
    unsafe_allow_html=True
)

# Chatbot UI
st.title("🚀 Career Guidance Chatbot 🎯")
st.write("Ask me career-related questions!")

# User Input
user_query = st.text_input("Type your question here:")

if user_query:
    # Check if the question exists in the dataset
    matched_row = data[data["Question"].str.lower() == user_query.lower()]
    
    if not matched_row.empty:
        answer = matched_row.iloc[0]["Answer"]
    else:
        answer = get_gemini_response(user_query)

    st.write("### Response:")
    st.write(answer)
