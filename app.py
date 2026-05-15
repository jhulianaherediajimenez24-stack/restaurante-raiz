from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# Esto es vital: permite que tu web se comunique con este servidor
CORS(app)

# Lista en memoria para guardar las reservas
reservas = []

@app.route('/')
def home():
    return "Servidor de RAÍZ encendido y funcionando", 200

# Esta ruta recibe los datos del formulario (index.html)
@app.route('/reservar', methods=['POST'])
def reservar():
    try:
        datos = request.json
        # Si el cliente no envió el estado, lo ponemos como Pendiente
        if 'estado' not in datos:
            datos['estado'] = 'Pendiente'
        
        reservas.append(datos)
        print(f"Nueva reserva recibida: {datos}") # Esto ayuda a ver errores en Render
        return jsonify({"status": "ok", "mensaje": "Reserva guardada correctamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 400

# Esta ruta le entrega la lista de reservas a tu panel (admin.html)
@app.route('/admin/reservas', methods=['GET'])
def ver_reservas():
    return jsonify(reservas), 200

# Esta ruta sirve para que tú confirmes las reservas desde el panel
@app.route('/admin/confirmar/<int:id>', methods=['POST'])
def confirmar_reserva(id):
    try:
        if 0 <= id < len(reservas):
            reservas[id]['estado'] = 'Confirmada'
            return jsonify({"status": "ok"}), 200
        return jsonify({"status": "error", "mensaje": "Reserva no encontrada"}), 404
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500

if __name__ == '__main__':
    # Render asigna el puerto automáticamente mediante la variable de entorno PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
