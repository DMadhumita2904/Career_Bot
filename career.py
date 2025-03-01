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

# Inject CSS for a smooth, light gradient animated background
st.markdown("""
    <style>
    @keyframes gradientChange {
        0% { background: linear-gradient(135deg, #FFD3A5, #FD6585); } /* Soft Peach to Pink */
        25% { background: linear-gradient(135deg, #A1C4FD, #C2E9FB); } /* Light Blue to Sky Blue */
        50% { background: linear-gradient(135deg, #FFDEE9, #B5FFFC); } /* Light Pink to Soft Aqua */
        75% { background: linear-gradient(135deg, #FAD961, #FFD452); } /* Warm Yellow */
        100% { background: linear-gradient(135deg, #FFD3A5, #FD6585); } /* Back to Soft Peach */
    }
    
    .stApp {
        animation: gradientChange 3s infinite alternate;
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)

# Reduce GIF size and center it
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.pinimg.com/originals/1f/f3/3e/1ff33ede4825194fdbcf0f9b5e27dc93.gif" width="250">
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
