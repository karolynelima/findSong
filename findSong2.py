import csv
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite conexões do frontend React

# Nome do arquivo CSV
arquivo_csv = "ariana_grande_albuns_musicas.csv"

# Carregar músicas do CSV para a memória
musicas = []
with open(arquivo_csv, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        musicas.append({
            "album": row["Álbum"],
            "titulo": row["Título da Música"],
            "letra": row["Letra"]
        })

# Rota para buscar músicas
@app.route('/buscar', methods=['POST'])
def buscar_musicas_por_frase():
    data = request.json
    frase = data.get('frase', '').lower()

    resultados = []
    padrao = re.compile(r'\b' + re.escape(frase) + r'\b', re.IGNORECASE)

    for musica in musicas:
        letra = musica["letra"].lower()
        linhas = letra.split("\n")

        for i, linha in enumerate(linhas):
            if padrao.search(linha):
                inicio = max(0, i - 3)
                fim = min(len(linhas), i + 4)
                estrofe_completa = "\n".join(linhas[inicio:fim]).strip()

                resultados.append({
                    "album": musica["album"],
                    "musica": musica["titulo"],
                    "estrofe": estrofe_completa
                })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
