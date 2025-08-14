from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = "vuelos.json"

# Función auxiliar: cargar datos
def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Función auxiliar: guardar datos  
def guardar_datos(datos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# Endpoint inicial
@app.route("/", methods=["GET"])
def inicio():
    return jsonify({"mensaje": "API de Vuelos"})

# GET - Listar todos los vuelos
@app.route("/api/vuelos", methods=["GET"])
def listar_vuelos():
    datos = cargar_datos()
    return jsonify(datos)

# GET - Obtener un vuelo por ID
@app.route("/api/vuelos/<int:vuelo_id>", methods=["GET"])
def obtener_vuelo(vuelo_id):
    datos = cargar_datos()
    for vuelo in datos:
        if vuelo["id"] == vuelo_id:
            return jsonify(vuelo)
    return jsonify({"error": "Vuelo no encontrado"}), 404

# POST - Agregar un nuevo vuelo
@app.route("/api/vuelos", methods=["POST"])
def agregar_vuelo():
    datos = cargar_datos()
    nuevo_vuelo = request.get_json()
    
    # Validación básica
    if not nuevo_vuelo.get("destino"):
        return jsonify({"error": "El campo 'destino' es obligatorio"}), 400
    
    # Asignar ID automático
    nuevo_vuelo["id"] = datos[-1]["id"] + 1 if datos else 1
    
    # Valores por defecto
    nuevo_vuelo.setdefault("capacidad", 100)
    nuevo_vuelo.setdefault("vendidos", 0)
    
    datos.append(nuevo_vuelo)
    guardar_datos(datos)
    return jsonify(nuevo_vuelo), 201

# PUT - Actualizar un vuelo por ID
@app.route("/api/vuelos/<int:vuelo_id>", methods=["PUT"])
def actualizar_vuelo(vuelo_id):
    datos = cargar_datos()
    vuelo_data = request.get_json()
    
    for vuelo in datos:
        if vuelo["id"] == vuelo_id:
            vuelo.update(vuelo_data)
            guardar_datos(datos)
            return jsonify(vuelo)
    return jsonify({"error": "Vuelo no encontrado"}), 404

# DELETE - Eliminar un vuelo por ID
@app.route("/api/vuelos/<int:vuelo_id>", methods=["DELETE"])
def eliminar_vuelo(vuelo_id):
    datos = cargar_datos()
    datos_filtrados = [vuelo for vuelo in datos if vuelo["id"] != vuelo_id]
    
    if len(datos) == len(datos_filtrados):
        return jsonify({"error": "Vuelo no encontrado"}), 404
    
    guardar_datos(datos_filtrados)
    return jsonify({"mensaje": f"Vuelo {vuelo_id} eliminado correctamente"})

if __name__ == "__main__":
    # Si no existe el archivo, crear uno vacío
    if not os.path.exists(DATA_FILE):
        guardar_datos([])
    app.run(debug=True)


# EJEMPLOS DE USO CON CURL:

# Crear vuelo:
# curl -X POST http://localhost:5000/api/vuelos \
#   -H "Content-Type: application/json" \
#   -d '{"destino": "Buenos Aires", "capacidad": 150}'

# Listar vuelos:
# curl http://localhost:5000/api/vuelos

# Ver vuelo específico:
# curl http://localhost:5000/api/vuelos/1

# Actualizar vuelo:
# curl -X PUT http://localhost:5000/api/vuelos/1 \
#   -H "Content-Type: application/json" \
#   -d '{"destino": "Córdoba", "vendidos": 25}'

# Eliminar vuelo:
# curl -X DELETE http://localhost:5000/api/vuelos/1