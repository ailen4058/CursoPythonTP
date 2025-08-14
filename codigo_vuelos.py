from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DATA_FILE = "vuelos.txt"

# Datos iniciales si el archivo no existe
#Crear una lista de vuelos con las siguientes categorías:

VUELOS_INICIALES = [
    {"codigo": "AR101", "destino": "Buenos Aires", "capacidad": 5, "vendidos": 0},
    {"codigo": "AR202", "destino": "Córdoba", "capacidad": 3, "vendidos": 0}
]

# Leer datos
def cargar_vuelos():
    if not os.path.exists(DATA_FILE):
        guardar_vuelos(VUELOS_INICIALES)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        vuelos = []
        for linea in f:
            partes = linea.strip().split(";")
            vuelos.append({
                "codigo": partes[0],
                "destino": partes[1],
                "capacidad": int(partes[2]),
                "vendidos": int(partes[3])
            })
        return vuelos

# Guardar datos
def guardar_vuelos(vuelos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for v in vuelos:
            f.write(f"{v['codigo']};{v['destino']};{v['capacidad']};{v['vendidos']}\n")

# Ver todos los vuelos
@app.route("/vuelos", methods=["GET"])
def listar_vuelos():
    return jsonify(cargar_vuelos())

# Ver vuelo por código
@app.route("/vuelos/<codigo>", methods=["GET"])
def ver_vuelo(codigo):
    vuelos = cargar_vuelos()
    for v in vuelos:
        if v["codigo"].lower() == codigo.lower():
            return jsonify(v)
    return jsonify({"error": "Vuelo no encontrado"}), 404

# Comprar pasaje
@app.route("/comprar", methods=["POST"])
def comprar():
    datos = request.get_json()
    codigo = datos.get("codigo", "").strip().upper()

    vuelos = cargar_vuelos()
    for v in vuelos:
        if v["codigo"] == codigo:
            if v["vendidos"] < v["capacidad"]:
                v["vendidos"] += 1
                guardar_vuelos(vuelos)
                return jsonify({"mensaje": f"Pasaje comprado para {codigo} - {v['destino']}"})
            else:
                return jsonify({"error": "No hay asientos disponibles"}), 400
    return jsonify({"error": "Vuelo no encontrado"}), 404

# Cancelar pasaje
@app.route("/cancelar", methods=["POST"])
def cancelar():
    datos = request.get_json()
    codigo = datos.get("codigo", "").strip().upper()

    vuelos = cargar_vuelos()
    for v in vuelos:
        if v["codigo"] == codigo:
            if v["vendidos"] > 0:
                v["vendidos"] -= 1
                guardar_vuelos(vuelos)
                return jsonify({"mensaje": f"Reserva cancelada en {codigo} - {v['destino']}"})
            else:
                return jsonify({"error": "No hay reservas para cancelar"}), 400
    return jsonify({"error": "Vuelo no encontrado"}), 404

if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        guardar_vuelos(VUELOS_INICIALES)
    app.run(debug=True)
