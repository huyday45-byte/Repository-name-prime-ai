import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

messages = [
    {
        "role": "system",
        "content": """
Bạn tên là Prime.
Bạn là trợ lý AI do Nguyễn Hồng Huy phát triển.
Không tự nhận là ChatGPT hay GPT-4.
Nếu không chắc thì hãy nói không chắc.
"""
    }
]

@app.route("/", methods=["GET", "POST"])
def home():
    reply = ""

    if request.method == "POST":
        user = request.form["message"]

        messages.append({
            "role": "user",
            "content": user
        })

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages
        )

        reply = response.choices[0].message.content

        messages.append({
            "role": "assistant",
            "content": reply
        })

    return render_template(
        "index.html",
        reply=reply
    )

if __name__ == "__main__":
    app.run(debug=True)