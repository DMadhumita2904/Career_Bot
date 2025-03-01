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

# Inject JavaScript to change background color dynamically
st.components.v1.html(
    """
    <script>
    let colors = ["#FCE4EC", "#E3F2FD", "#E8F5E9", "#FFFDE7", "#F3E5F5", "#E0F7FA", "#FFEBEE"];
    let index = 0;
    function changeColor() {
        document.body.style.transition = "background-color 2s ease-in-out";
        document.body.style.backgroundColor = colors[index];
        index = (index + 1) % colors.length;
    }
    setInterval(changeColor, 3000);
    </script>
    """,
    height=0,
)

# Reduce GIF size and center it
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://cdn.pixabay.com/animation/2022/10/06/09/57/09-57-46-893_512.gif" width="250">
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
