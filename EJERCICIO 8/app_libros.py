# LABORATORIO 22 - EJERCICIO 8
# AUTORA: Velasquez Puma Brigitte Karolay

import json

libros = []
_next_id = 1

def _read_json_from_environ(environ):
    length = int(environ.get("CONTENT_LENGTH", 0) or 0)
    if length == 0:
        return {}
    body = environ["wsgi.input"].read(length).decode("utf-8")
    return json.loads(body)

def app(environ, start_response):
    global _next_id
    path = environ.get("PATH_INFO", "")
    method = environ.get("REQUEST_METHOD", "GET")

 
    if method == "GET" and path == "/libros":
        start_response("200 OK", [("Content-Type", "application/json; charset=utf-8")])
        return [json.dumps(libros).encode("utf-8")]


    if method == "POST" and path == "/libros":
        try:
            data = _read_json_from_environ(environ)
            titulo = data["titulo"]
            autor = data["autor"]
            anio = int(data["anio"])
        except Exception:
            start_response("400 Bad Request", [("Content-Type", "text/plain; charset=utf-8")])
            return [b"JSON invalido o campos faltantes"]

        libro = {"id": _next_id, "titulo": titulo, "autor": autor, "anio": anio}
        _next_id += 1
        libros.append(libro)
        start_response("201 Created", [("Content-Type", "application/json; charset=utf-8")])
        return [json.dumps(libro).encode("utf-8")]


    if method == "GET" and path.startswith("/libros/"):
        try:
            id_req = int(path.rsplit("/", 1)[-1])
        except ValueError:
            start_response("400 Bad Request", [("Content-Type", "text/plain; charset=utf-8")])
            return [b"ID invalido"]
        for l in libros:
            if l["id"] == id_req:
                start_response("200 OK", [("Content-Type", "application/json; charset=utf-8")])
                return [json.dumps(l).encode("utf-8")]
        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"No encontrado"]

    start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Ruta no encontrada"]
