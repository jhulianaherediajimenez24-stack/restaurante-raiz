from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

reservas = []

@app.route('/')
def home():
    return "SERVIDOR RAÍZ: FUNCIONANDO", 200

@app.route('/reservar', methods=['POST'])
def reservar():
    try:
        datos = request.json
        # Guardamos todos los datos que vienen de la web
        reserva = {
            "nombre": datos.get('nombre'),
            "celular": datos.get('celular'),
            "correo": datos.get('correo'), # <-- AQUÍ GUARDAMOS EL CORREO
            "fecha": datos.get('fecha'),
            "hora": datos.get('hora'),
            "personas": datos.get('personas'),
            "ocasion": datos.get('ocasion'),
            "ubicacion": datos.get('ubicacion'),
            "alergias": datos.get('alergias', 'Ninguna'),
            "estado": "Pendiente"
        }
        reservas.append(reserva)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 400

@app.route('/admin/reservas', methods=['GET'])
def ver_reservas():
    return jsonify(reservas), 200

@app.route('/admin/confirmar/<int:id>', methods=['POST'])
def confirmar_reserva(id):
    try:
        datos = request.json
        nuevo_estado = datos.get('estado', 'Aprobada')
        if 0 <= id < len(reservas):
            reservas[id]['estado'] = nuevo_estado
            return jsonify({"status": "ok"}), 200
        return jsonify({"status": "error"}), 404
    except Exception as e:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
