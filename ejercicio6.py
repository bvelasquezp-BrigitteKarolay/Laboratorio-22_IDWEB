# LABORATORIO 22 - EJERCICIO 6
# AUTORA: Velasquez Puma Brigitte Karolay

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))
            a = data.get("a")
            b = data.get("b")
            suma = a + b
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"suma": suma}).encode("utf-8"))
        except Exception:
            self.send_response(400)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8001), Handler)
    print("Servidor POST-suma en http://localhost:8001")
    server.serve_forever()
