import lyricsgenius
import time
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from requests.exceptions import Timeout
from waitress import serve

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

genius = lyricsgenius.Genius("ZU-1J5vzPA1kzDOXWTMWMohIloyRiUafyhnSwXfGeMptN5JwMj1xpjQ4iC0Q3IMW", timeout=30)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar_musicas_por_frase():
    data = request.json
    cantor = data.get('cantor')
    frase = data.get('frase')

    try:
        # Busca o artista
        artista = genius.search_artist(cantor, max_songs=10, sort="popularity")
        
        # Lista para armazenar as músicas e as estrofes que contêm a frase
        resultados = []
        estrofes_vistas = set()  # Conjunto para evitar repetições
        
        # Prepara a expressão regular para buscar a frase completa
        padrao = re.compile(r'\b' + re.escape(frase.lower()) + r'\b', re.IGNORECASE)
        
         # Itera sobre as músicas do artista
        for musica in artista.songs:
            letra = musica.lyrics.lower()
            linhas = letra.split("\n")  # Divide a letra em linhas
            
            # Itera sobre cada linha para encontrar a frase
            for i, linha in enumerate(linhas):
                if padrao.search(linha):
                    # Pegamos a estrofe completa (3 linhas antes e 3 depois para contexto)
                    inicio = max(0, i - 3)
                    fim = min(len(linhas), i + 4)  # Inclui a linha com a frase
                    estrofe_completa = "\n".join(linhas[inicio:fim]).strip()

                    # Se a estrofe já foi adicionada, não adiciona novamente
                    if estrofe_completa not in estrofes_vistas:
                        estrofes_vistas.add(estrofe_completa)  # Adiciona ao conjunto
                        resultados.append({
                            "musica": musica.title,
                            "estrofe": estrofe_completa
                        })
        
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    print("Servidor rodando com Waitress...")
    serve(app, host="0.0.0.0", port=8000)

# def salvar_resultados_txt(resultados, arquivo):
#     """Salva os resultados em um arquivo .txt."""
#     with open(arquivo, "w", encoding="utf-8") as f:
#         for resultado in resultados:
#             f.write(f"Música: {resultado['musica']}\n")
#             f.write(f"Estrofe: {resultado['estrofe']}\n")
#             f.write("-" * 50 + "\n")

# def salvar_resultados_csv(resultados, arquivo):
#     """Salva os resultados em um arquivo .csv."""
#     import csv
#     with open(arquivo, "w", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow(["Música", "Estrofe"])  # Cabeçalho
#         for resultado in resultados:
#             writer.writerow([resultado['musica'], resultado['estrofe']])

# # Exemplo de uso
# cantor = input("Digite o nome do cantor: ")
# frase = input("Digite a palavra ou frase que deseja buscar: ")
# resultados = buscar_musicas_por_frase(cantor, frase)

# print(f"\nResultados para a frase '{frase}' nas músicas de {cantor}:\n")
# for resultado in resultados:
#     print(f"Música: {resultado['musica']}")
#     print(f"Estrofe: {resultado['estrofe']}")
#     print("-" * 50)

# # Salvar resultados
# if resultados:
#     opcao = input("\nDeseja salvar os resultados? (S/N): ").strip().lower()
#     if opcao == "s":
#         formato = input("Salvar como (1) TXT ou (2) CSV? Digite 1 ou 2: ").strip()
#         if formato == "1":
#             arquivo = f"resultados_{cantor}_{frase}.txt"
#             salvar_resultados_txt(resultados, arquivo)
#             print(f"Resultados salvos em {arquivo}")
#         elif formato == "2":
#             arquivo = f"resultados_{cantor}_{frase}.csv"
#             salvar_resultados_csv(resultados, arquivo)
#             print(f"Resultados salvos em {arquivo}")
#         else:
#             print("Opção inválida. Nada foi salvo.")
# else:
#     print("Nenhum resultado encontrado para salvar.")