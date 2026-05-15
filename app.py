from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# Importante: Esto permite que tu web (la computadora) hable con este cerebro (el mundo)
CORS(app)

# Aquí se guardan las reservas en la memoria del servidor
reservas = []

@app.route('/')
def home():
    return "SERVIDOR RAÍZ: FUNCIONANDO", 200

# Ruta para recibir las reservas del formulario de clientes
@app.route('/reservar', methods=['POST'])
def reservar():
    try:
        datos = request.json
        if not datos:
            return jsonify({"status": "error", "mensaje": "No hay datos"}), 400
        
        # Agregamos estado pendiente por defecto
        datos['estado'] = 'Pendiente'
        reservas.append(datos)
        print(f"Reserva recibida: {datos}")
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 400

# Ruta para que el panel de administrador vea la lista
@app.route('/admin/reservas', methods=['GET'])
def ver_reservas():
    return jsonify(reservas), 200

# Ruta para que tú confirmes una reserva desde el panel
@app.route('/admin/confirmar/<int:id>', methods=['POST'])
def confirmar_reserva(id):
    try:
        if 0 <= id < len(reservas):
            reservas[id]['estado'] = 'Confirmada'
            return jsonify({"status": "ok"}), 200
        return jsonify({"status": "error"}), 404
    except Exception as e:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    # Usamos el puerto que Render nos asigne
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
