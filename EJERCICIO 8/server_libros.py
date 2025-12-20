# LABORATORIO 22 - EJERCICIO 8

from wsgiref.simple_server import make_server
from app_libros import app

if __name__ == "__main__":
    server = make_server("localhost", 8003, app)
    print("Servidor libros en http://localhost:8003")
    server.serve_forever()
