from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
from transformers import pipeline
import re
import ssl
import certifi

ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

app = Flask(__name__)

# Cargamos un modelo local de generación de texto (GPT-2 reducido)
text_generator = pipeline("text-generation", model="distilgpt2")

def extract_text_from_pdf(pdf_file):
    """Extrae y limpia el texto de un PDF."""
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + " "
    
    # Limpieza del texto: eliminar caracteres raros y espacios extras
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_ai_response(text, user_content):
    """Genera una respuesta usando GPT-2 basado en la consulta y el contenido del PDF."""
    prompt = f"Usuario: {user_content}\nDocumento: {text}\nRespuesta:"
    
    # Generar respuesta con el modelo local
    response = text_generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]
    
    # Limpiar la respuesta para que no repita el prompt completo
    response = response.replace(prompt, "").strip()
    
    return response

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
            combined_text += f"{text} "

        recommendation = generate_ai_response(combined_text, user_content)
        return jsonify({"recommendation": recommendation})
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
