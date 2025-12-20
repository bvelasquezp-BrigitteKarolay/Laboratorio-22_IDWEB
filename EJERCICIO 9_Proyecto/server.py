# LABORATORIO 22 - EJERCICIO 9
# AUTORA: Velasquez Puma Brigitte Karolay

from wsgiref.simple_server import make_server
from urllib.parse import unquote
import json
import os
import mimetypes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

equipos = [
    {"id": 1, "nombre": "Real Madrid", "ciudad": "Madrid", "nivelAtaque": 10, "nivelDefensa": 9},
    {"id": 2, "nombre": "Barcelona", "ciudad": "Barcelona", "nivelAtaque": 9, "nivelDefensa": 8},
    {"id": 3, "nombre": "Melgar", "ciudad": "Arequipa", "nivelAtaque": 5, "nivelDefensa": 4}
]

next_id = 4

def servir_estatico(path):
    ruta = path.replace("/static/", "")
    archivo = os.path.join(STATIC_DIR, ruta)

    if not os.path.isfile(archivo):
        return None, None

    content_type, _ = mimetypes.guess_type(archivo)
    if content_type is None:
        content_type = "application/octet-stream"

    with open(archivo, "rb") as f:
        return f.read(), content_type

def leer_json(environ):
    length = int(environ.get("CONTENT_LENGTH", 0))
    if length == 0:
        return {}
    body = environ["wsgi.input"].read(length).decode("utf-8")
    return json.loads(body)

def app(environ, start_response):
    global next_id

    method = environ["REQUEST_METHOD"]
    path = unquote(environ["PATH_INFO"])

    if path.startswith("/static/"):
        contenido, tipo = servir_estatico(path)
        if contenido is None:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Archivo no encontrado"]
        start_response("200 OK", [("Content-Type", tipo)])
        return [contenido]

    if method == "GET" and path == "/":
        contenido, tipo = servir_estatico("/static/index.html")
        if contenido is None:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Index no encontrado"]
        start_response("200 OK", [("Content-Type", tipo)])
        return [contenido]

    if method == "GET" and path == "/equipos":
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(equipos).encode("utf-8")]

    if method == "GET" and path.startswith("/equipos/"):
        try:
            eid = int(path.split("/")[-1])
        except ValueError:
            start_response("400 Bad Request", [("Content-Type", "text/plain")])
            return [b"ID invalido"]

        for e in equipos:
            if e["id"] == eid:
                start_response("200 OK", [("Content-Type", "application/json")])
                return [json.dumps(e).encode("utf-8")]

        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Equipo no encontrado"]

    if method == "POST" and path == "/equipos":
        try:
            data = leer_json(environ)
            equipo = {
                "id": next_id,
                "nombre": data["nombre"],
                "ciudad": data["ciudad"],
                "nivelAtaque": int(data["nivelAtaque"]),
                "nivelDefensa": int(data["nivelDefensa"])
            }

            if not (1 <= equipo["nivelAtaque"] <= 10 and 1 <= equipo["nivelDefensa"] <= 10):
                raise ValueError

            equipos.append(equipo)
            next_id += 1

            start_response("201 Created", [("Content-Type", "application/json")])
            return [json.dumps(equipo).encode("utf-8")]

        except Exception:
            start_response("400 Bad Request", [("Content-Type", "text/plain")])
            return [b"Datos invalidos"]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Ruta no encontrada"]

if __name__ == "__main__":
    print("Servidor WSGI en http://localhost:8004")
    server = make_server("localhost", 8004, app)
    server.serve_forever()
