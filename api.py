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
You are Lokesh's professional AI assistant. Answer only based on the following profile:
{json.dumps(profile_data, indent=2)}
Question: "{question}"
Only respond to professional queries. If the question is personal, politely state it's outside your scope.
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