from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
from openai import OpenAI
import httpx
import os

app = Flask(__name__)

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1",
    http_client=httpx.Client(verify=False)
)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_recommendation(text, user_content):
    chat = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[
            {
                "role": "user",
                "content": f"{user_content}\n\n{text}"
            }
        ]
    )
    return chat.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_content = request.form.get("user_content")
        files = request.files.getlist("files")
        
        if not user_content or not files:
            return jsonify({"error": "Por favor, ingresa un contenido personalizado y sube al menos un archivo PDF."})
        
        combined_text = ""
        for file in files:
            text = extract_text_from_pdf(file)
            combined_text += f"--- Contenido de {file.filename} ---\n{text}\n\n"
        
        recommendation = get_recommendation(combined_text, user_content)
        return jsonify({"recommendation": recommendation})
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)