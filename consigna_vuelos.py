from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DATA_FILE = "vuelos.txt"

# Datos iniciales si el archivo no existe
# Crear una lista de vuelos con las siguientes categorías:
#  {"codigo": "", "destino": "", "capacidad": , "vendidos": },
# Ejemplo: {"codigo": "AA123", "destino": "Buenos Aires", "capacidad": 150, "vendidos": 0},   
VUELOS_INICIALES = [
    
]

# Crea una función cargar_vuelos() que lea el archivo vuelos.txt y retorne una lista de diccionarios con los datos de los vuelos.
# La función debe:
# 1. Verificar si el archivo existe, si no existe, crear uno con los vuelos iniciales
# 2. Leer el archivo línea por línea
# 3. Separar cada línea por ";" para obtener: codigo, destino, capacidad, vendidos
# 4. Convertir capacidad y vendidos a enteros
# 5. Retornar una lista de diccionarios con la estructura: {"codigo": "", "destino": "", "capacidad": 0, "vendidos": 0}
def cargar_vuelos():
    pass

# Crea una función guardar_vuelos() que reciba una lista de vuelos y los guarde en el archivo vuelos.txt
# con el formato: codigo;destino;capacidad;vendidos (uno por línea)
# La función debe:
# 1. Abrir el archivo en modo escritura con encoding utf-8
# 2. Iterar sobre cada vuelo en la lista
# 3. Escribir cada vuelo en formato: codigo;destino;capacidad;vendidos\n
def guardar_vuelos(vuelos):
    pass

# Crea un endpoint GET /vuelos que devuelva todos los vuelos en formato JSON
# Usa la función cargar_vuelos() y jsonify() para retornar los datos
@app.route("/vuelos", methods=["GET"])
def listar_vuelos():
    pass

# Crea un endpoint GET /vuelos/<codigo> que devuelva la información de un vuelo específico por su código
# Si no encuentra el vuelo, debe devolver un error 404 con el mensaje "Vuelo no encontrado"
# La función debe:
# 1. Cargar todos los vuelos
# 2. Buscar el vuelo que coincida con el código (ignorando mayúsculas/minúsculas)
# 3. Si lo encuentra, retornar el vuelo en JSON
# 4. Si no lo encuentra, retornar {"error": "Vuelo no encontrado"} con código 404
@app.route("/vuelos/<codigo>", methods=["GET"])
def ver_vuelo(codigo):
    pass

# Crea un endpoint POST /comprar que reciba un JSON con el código del vuelo
# Si hay asientos disponibles (vendidos < capacidad), incrementa los vendidos en 1
# Si no hay asientos disponibles, devuelve error 400 con mensaje "No hay asientos disponibles"
# Si el vuelo no existe, devuelve error 404 con mensaje "Vuelo no encontrado"
# La función debe:
# 1. Obtener los datos JSON de la petición
# 2. Extraer el código del vuelo y convertirlo a mayúsculas
# 3. Cargar todos los vuelos
# 4. Buscar el vuelo por código
# 5. Verificar disponibilidad y actualizar si es posible
# 6. Guardar los cambios y retornar mensaje de confirmación
@app.route("/comprar", methods=["POST"])
def comprar():
    pass

# Crea un endpoint POST /cancelar que reciba un JSON con el código del vuelo
# Si hay reservas (vendidos > 0), decrementa los vendidos en 1
# Si no hay reservas para cancelar, devuelve error 400 con mensaje "No hay reservas para cancelar"
# Si el vuelo no existe, devuelve error 404 con mensaje "Vuelo no encontrado"
# La función debe:
# 1. Obtener los datos JSON de la petición
# 2. Extraer el código del vuelo y convertirlo a mayúsculas
# 3. Cargar todos los vuelos
# 4. Buscar el vuelo por código
# 5. Verificar que hay reservas para cancelar y actualizar si es posible
# 6. Guardar los cambios y retornar mensaje de confirmación
@app.route("/cancelar", methods=["POST"])
def cancelar():
    pass

# Al ejecutar el archivo, verifica si existe el archivo de datos
# Si no existe, crea el archivo con los vuelos iniciales y ejecuta la aplicación en modo debug
if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        guardar_vuelos(VUELOS_INICIALES)
    app.run(debug=True)