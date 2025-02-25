from flask import Flask, jsonify
import os  # Necesario para el puerto en Render

app = Flask(__name__)

# Ruta de prueba para verificar que la API está activa
@app.route('/')
def home():
    return jsonify({
        "status": "API operativa",
        "ruta_chat": "/api/chat (POST)"
    })

# Ruta principal de tu funcionalidad
@app.route('/api/chat', methods=['POST'])
def handle_chat():
    # ... (tu lógica aquí)
    return jsonify({"reply": "Respuesta desde Render"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ¡Clave para Render!
    app.run(host='0.0.0.0', port=port)  # Usa el puerto de Render