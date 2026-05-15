from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# Esto permite que tu web (raiz-oficial) se comunique con este cerebro
CORS(app)

# Aquí se guardarán las reservas temporalmente
reservas = []

@app.route('/')
def home():
    return "Servidor de RAÍZ encendido y funcionando", 200

# Ruta para recibir reservas desde el formulario
@app.route('/reservar', methods=['POST'])
def reservar():
    try:
        datos = request.json
        # Ponemos estado pendiente por defecto si no viene
        if 'estado' not in datos:
            datos['estado'] = 'Pendiente'
        reservas.append(datos)
        return jsonify({"status": "ok", "mensaje": "Reserva recibida"}), 200
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 400

# Ruta para que tú veas las reservas en el panel admin.html
@app.route('/admin/reservas', methods=['GET'])
def ver_reservas():
    return jsonify(reservas), 200

# Ruta para que confirmes una reserva
@app.route('/admin/confirmar/<int:id>', methods=['POST'])
def confirmar_reserva(id):
    if 0 <= id < len(reservas):
        reservas[id]['estado'] = 'Confirmada'
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    # Render asigna el puerto automáticamente
    app.run(host='0.0.0.0', port=os.getenv("PORT", default=5000))
