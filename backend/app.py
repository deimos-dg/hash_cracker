from flask import Flask, request, jsonify
from flask_cors import CORS
from hash_cracker import cracker
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Habilitar CORS para Vue.js


@app.route('/api/identify-hash', methods=['POST'])
def identify_hash():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos JSON'}), 400

        hash_input = data.get('hash', '').strip()

        if not hash_input:
            return jsonify({'error': 'Hash no proporcionado'}), 400

        logger.info(f"Identificando hash: {hash_input}")
        result = cracker.identify_hash(hash_input)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error en identify-hash: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@app.route('/api/crack-hash', methods=['POST'])
def crack_hash():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos JSON'}), 400

        target_hash = data.get('hash', '').strip().lower()
        algorithm = data.get('algorithm', '')
        method = data.get('method', 'common')

        if not target_hash:
            return jsonify({'error': 'Hash no proporcionado'}), 400
        if not algorithm:
            return jsonify({'error': 'Algoritmo no especificado'}), 400

        logger.info(f"Crackeando hash {algorithm}: {target_hash}")

        # Seleccionar wordlist según método
        if method == 'common':
            wordlist = cracker.common_passwords
        else:
            return jsonify({'error': 'Método no implementado'}), 400

        result = cracker.crack_hash(target_hash, algorithm, wordlist)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error en crack-hash: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@app.route('/api/stop-crack', methods=['POST'])
def stop_crack():
    try:
        cracker.stop_current_operation()
        logger.info("Operación de cracking detenida")
        return jsonify({'message': 'Operación detenida'})
    except Exception as e:
        logger.error(f"Error en stop-crack: {str(e)}")
        return jsonify({'error': 'Error al detener la operación'}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        return jsonify({
            'common_passwords_count': len(cracker.common_passwords),
            'status': 'ready',
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Error en stats: {str(e)}")
        return jsonify({'error': 'Error al obtener estadísticas'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'hash-cracker-api'})


if __name__ == '__main__':
    print("🚀 Starting Hash Cracker API Server...")
    print("📊 Available endpoints:")
    print("   POST /api/identify-hash")
    print("   POST /api/crack-hash")
    print("   POST /api/stop-crack")
    print("   GET  /api/stats")
    print("   GET  /api/health")
    print("🌐 Server running on http://localhost:5000")

    app.run(debug=True, port=5000, host='0.0.0.0')