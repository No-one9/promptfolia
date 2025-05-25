from flask import Flask, render_template, request, session, Response
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'lokesh-secret'

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

with open("myprofile.json", "r") as f:
    profile_data = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    answer = ""
    last_question = ""

    if request.method == "POST":
        question = request.form["question"]
        last_question = question
        if question.strip():
            prompt = f"""
You are Lokesh's professional AI assistant. You are confident, direct, and highlight his strengths assertively. Use only the following profile data to answer:
{json.dumps(profile_data, indent=2)}
If a question is about anything outside this scope (e.g., general knowledge, politics, entertainment), politely respond with:
"I'm Lokesh’s professional assistant and I can only answer questions about Lokesh’s experience, skills, and projects."
Question: "{question}"

- Always assume the intent is professional.
- If the profile has relevant data, answer decisively and affirmatively.
- If the profile lacks explicit details but implies capability, confidently infer from experience and use professional language to support the answer.
- Only when it's absolutely out of scope, respond that the answer cannot be provided.
"""
            try:
                response = model.generate_content(prompt)
                answer = response.text
                session["chat_history"].append({
                    "question": question,
                    "answer": answer
                })
                session.modified = True
                last_question = ""  # Clear the textarea on success
            except Exception as e:
                answer = f"Error: {str(e)}"

    return render_template("index.html", chat_history=session["chat_history"], answer=answer, last_question=last_question)



# Export chat feature
@app.route("/export", methods=["GET"])
def export_chat():
    chat_log = session.get("chat_history", [])
    export_text = ""
    for item in chat_log:
        export_text += f"Q: {item['question']}\nA: {item['answer']}\n\n"
    return Response(
        export_text,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=\"lokesh's_AI_Assistant_chat.txt\""}
    )
@app.route("/clear", methods=["POST"])
def clear_chat():
    session["chat_history"] = []
    session.modified = True
    return "", 204  # No content

if __name__ == '__main__':
    app.run(debug=True)