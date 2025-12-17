# LABORATORIO 22 - EJERCICIO 4
# AUTORA: Velasquez Puma Brigitte Karolay

import urllib.request
import json
import ssl

def listar_10_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon?limit=10&offset=0"
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "python-urllib/3"})
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        body = resp.read().decode("utf-8")
    data = json.loads(body)
    resultados = data.get("results", [])
    print("Primeros 10 Pokémon (nombres):")
    for i, p in enumerate(resultados, start=1):
        print(f"{i}. {p.get('name')}")

if __name__ == "__main__":
    try:
        listar_10_pokemon()
    except Exception as e:
        print("Error al consultar PokéAPI:", e)
