import streamlit as st
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load Gemini API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# print("Available models:")
# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Load your profile JSON data
with open('myprofile.json', 'r') as f:
    profile_data = json.load(f)

# Define Gemini query function
def query_profile(question):
    prompt = f"""
    You are Lokesh's professional AI assistant. You are only allowed to answer questions related to his professional profile such as education, skills, experience, certifications, or job qualifications.
    If the question is personal (e.g., about relationships, religion, politics, hobbies, etc.), respond politely but firmly that the assistant is limited to professional topics.
    Here is Lokesh's professional profile:
    {json.dumps(profile_data, indent=2)}

    Answer the following question based solely on the professional profile:

    Question: "{question}"
    """

    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit User Interface
st.set_page_config(page_title="Lokesh's AI Profile Assistant")
st.title("Lokesh's AI-powered Professional Profile Assistant")

user_question = st.text_area("Ask any professional question about Lokesh:", height=150)

if st.button("Get Answer"):
    if user_question.strip():
        with st.spinner("Generating answer..."):
            answer = query_profile(user_question)
        st.success("Here's your answer:")
        st.markdown(answer)
    else:
        st.warning("Please enter a valid question.")