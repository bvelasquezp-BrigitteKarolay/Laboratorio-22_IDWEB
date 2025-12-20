# LABORATORIO 22 - EJERCICIO 4
# AUTORA: Velasquez Puma Brigitte Karolay

import urllib.request
import json
import ssl

def listar_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon?limit=10"
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "python-urllib/3"})
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode())

    for p in data["results"]:
        print(p["name"])

if __name__ == "__main__":
    listar_pokemon()
