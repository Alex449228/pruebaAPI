from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite todas las origins (ajusta en producción)

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
        
        # Validación básica del request
        if not data or 'message' not in data:
            return jsonify({'error': 'Formato de mensaje inválido'}), 400
        
        user_message = data['message']
        
        # Aquí iría tu lógica de IA/procesamiento
        ai_response = f"Recibí tu mensaje: '{user_message}'. Esto es una respuesta de prueba desde la API Python."
        
        return jsonify({
            'reply': ai_response,
            'status': 'success'
        }), 200

    except Exception as e:
        app.logger.error(f'Error en handle_chat: {str(e)}')
        return jsonify({
            'error': 'Error interno del servidor',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # debug=False en producción