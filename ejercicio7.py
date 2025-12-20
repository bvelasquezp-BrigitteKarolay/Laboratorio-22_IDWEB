# LABORATORIO 22 - EJERCICIO 7
# AUTORA: Velasquez Puma Brigitte Karolay

from wsgiref.simple_server import make_server

def app(environ, start_response):
    path = environ.get("PATH_INFO", "")
    if path == "/":
        start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Inicio"]
    elif path == "/saludo":
        start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Hola mundo desde WSGI"]
    else:
        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"No encontrado"]

if __name__ == "__main__":
    server = make_server("localhost", 8002, app)
    print("WSGI en http://localhost:8002")
    server.serve_forever()
