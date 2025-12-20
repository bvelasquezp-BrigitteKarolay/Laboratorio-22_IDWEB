# LABORATORIO 22 - EJERCICIO 5
# AUTORA: Velasquez Puma Brigitte Karolay

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = "<!doctype html><html><head><meta charset='utf-8'><title>Index</title></head><body><h1>HTML estatico</h1></body></html>"
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/saludo":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"msg": "Hola"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    print("Servidor HTTP en http://localhost:8000")
    server.serve_forever()
