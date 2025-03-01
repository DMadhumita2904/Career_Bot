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
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        return response.text if response else "I'm sorry, I couldn't generate a response."
    except Exception as e:
        return "I'm sorry, there was an error processing your request."

# Initialize session state for chat history and user input
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Gradient background colors
gradient_colors = [
    "#FFDEE9, #B5FFFC", "#A1C4FD, #C2E9FB", "#FFEFBA, #FFFFFF",
    "#FAACA8, #DDD6F3", "#FAD961, #F76B1C", "#FDCB82, #FF9A8B",
    "#A18CD1, #FBC2EB", "#F7CE68, #FBAB7E", "#70F570, #49C628",
    "#30Cfd0, #330867", "#667eea, #764ba2", "#FF9A9E, #FAD0C4"
]

# Inject CSS for dynamic background and chat bubbles
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
    .stApp {{ animation: gradientChange 15s infinite alternate; background-size: cover; }}

    .bot-message {{
        background-color: #f0f0f5; color: #333; padding: 10px 15px;
        border-radius: 10px; width: fit-content; max-width: 70%;
        margin: 10px 0; text-align: left; font-family: Arial, sans-serif;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }}

    .user-message {{
        background-color: #0078ff; color: white; padding: 10px 15px;
        border-radius: 10px; width: fit-content; max-width: 70%;
        margin: 10px 0 10px auto; text-align: right; font-family: Arial, sans-serif;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Display animated GIF at the top
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.pinimg.com/originals/1f/f3/3e/1ff33ede4825194fdbcf0f9b5e27dc93.gif" width="300" height="200">
    </div>
    """,
    unsafe_allow_html=True
)

# Chatbot UI
st.title("🚀 Career Guidance Chatbot 🎯")
st.write("Ask me career-related questions!")

# Form for user input (keeps input box at the bottom)
with st.form(key="query_form"):
    user_query = st.text_input("Type your question here:", value=st.session_state["user_input"], key="user_query")
    submit_button = st.form_submit_button("Ask")

if submit_button and user_query.strip():
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "text": user_query})

    # Check if the question exists in the dataset
    matched_row = data[data["Question"].str.contains(user_query, case=False, na=False)]

    if not matched_row.empty:
        answer = matched_row.iloc[0]["Answer"]
    else:
        answer = get_gemini_response(user_query)

    # Add bot response to session state
    st.session_state.messages.append({"role": "bot", "text": answer})

    # Clear input after submission
    st.session_state["user_input"] = ""

# Display chat messages with better UI
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["text"]}</div>', unsafe_allow_html=True)
