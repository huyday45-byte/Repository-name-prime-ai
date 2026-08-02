import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from openai import OpenAI
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
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
Nếu đưa dữ liệu cho người dùng, thì hãy liệt kê lần lượt, ko được tạo khung hay lập bảng.
Không được đưa hình ảnh cho người dùng.
Bạn không có quyền lập bảng, tạo khung.
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
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "Không có file"

        file = request.files["file"]

        if file.filename == "":
            return "Chưa chọn file"

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        return f"Đã tải lên: {filename}"

    return render_template("upload.html")