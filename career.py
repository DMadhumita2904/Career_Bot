import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# Set Streamlit page configuration
st.set_page_config(page_title="Career Guidance Chatbot", page_icon="🎯", layout="centered")

# Load the dataset with caching
@st.cache_data
def load_data():
    return pd.read_csv("profession_questions_answers.csv")

df = load_data()

def get_predefined_answer(profession, question):
    """Fetch the predefined answer from the dataset."""
    row = df[(df["Profession"] == profession) & (df["Question"] == question)]
    return row["Answer"].values[0] if not row.empty else None

# Set up Gemini API with proper configuration
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])  # Use Streamlit secrets management
except Exception as e:
    st.error("Error configuring Gemini API. Please check your API key configuration.")
    st.stop()

@st.cache_data(ttl=3600)  # Cache responses for 1 hour
def get_gemini_response(question):
    """Fetch additional insights from Gemini AI with error handling."""
    try:
        model = genai.GenerativeModel("gemini-pro")  # Use faster model
        response = model.generate_content(
            question,
            generation_config={"temperature": 0.5},
            request_options={"timeout": 10}  # 10-second timeout
        )
        return response.text
    except Exception as e:
        return f"⚠️ Couldn't fetch additional insights: {str(e)}"

# Streamlit UI with enhanced design
st.markdown("""
    <style>
    .main {background-color: #f4f4f4;}
    .stTextInput, .stSelectbox {border-radius: 10px;}
    .stButton button {background-color: #4CAF50; color: white; font-size: 18px; padding: 10px;}
    .response-section {padding: 20px; border-radius: 10px; margin: 15px 0;}
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Career Guidance Chatbot")
st.caption("Get expert insights and guidance for your career path.")

st.markdown("""
    ### 🔍 How It Works:
    1. Select a profession from the dropdown
    2. Choose a career-related question
    3. Get expert advice and AI-powered insights!
""")

# User input
profession = st.selectbox("🔹 Choose a profession:", df["Profession"].unique())
question = st.selectbox("🔹 Choose a question:", df[df["Profession"] == profession]["Question"].unique())

if st.button("✨ Get Answer ✨"):
    start_time = datetime.now()
    
    # Get predefined answer immediately
    predefined_answer = get_predefined_answer(profession, question)
    
    # Display results in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='response-section' style='background-color: #e8f5e9;'>", unsafe_allow_html=True)
        st.subheader("📌 Predefined Answer:")
        st.write(predefined_answer)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='response-section' style='background-color: #e3f2fd;'>", unsafe_allow_html=True)
        st.subheader("🤖 AI Insights:")
        with st.spinner("Generating additional insights..."):
            gemini_answer = get_gemini_response(question)
            st.write(gemini_answer)
        st.markdown(f"⏱️ Response time: {(datetime.now() - start_time).total_seconds():.1f}s")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    ---
    **💡 Pro Tip:** Keep exploring different professions and questions to find your perfect career path!
""")

