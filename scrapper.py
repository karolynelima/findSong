import lyricsgenius
import csv
import time

# Inicializa a API do Genius com timeout maior
genius = lyricsgenius.Genius("ZU-1J5vzPA1kzDOXWTMWMohIloyRiUafyhnSwXfGeMptN5JwMj1xpjQ4iC0Q3IMW", timeout=30)

# Configurações para melhor formatação
genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]

# Nome do artista
artista_nome = "Ariana Grande"

# Lista de álbuns da artista
lista_de_albuns = [
    "Yours Truly",
    "My Everything",
    "Dangerous Woman",
    "Sweetener",
    "Thank U, Next",
    "Positions",
    "eternal sunshine"
]

# Nome do arquivo CSV
arquivo_csv = "ariana_grande_albuns_musicas.csv"

# Criar e escrever o cabeçalho do CSV
with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Álbum", "Título da Música", "Letra"])  # Cabeçalho

    # Buscar cada álbum manualmente e salvar suas músicas
    for album_titulo in lista_de_albuns:
        print(f"Buscando músicas do álbum: {album_titulo}...")

        tentativas = 3  # Tenta buscar até 3 vezes em caso de erro
        while tentativas > 0:
            try:
                album_completo = genius.search_album(album_titulo, artista_nome)

                # Se o álbum não for encontrado, não tenta novamente
                if album_completo is None:
                    print(f"Álbum {album_titulo} não encontrado.")
                    break

                # Verifica se há faixas no álbum
                if not hasattr(album_completo, 'tracks'):
                    print(f"Erro: O álbum {album_titulo} não contém músicas.")
                    break

                # Itera sobre as faixas do álbum
                for track in album_completo.tracks:
                    if hasattr(track, 'song'):
                        musica = track.song
                        writer.writerow([album_titulo, musica.title, musica.lyrics])

                break  # Sai do loop se não houver erro

            except Exception as e:
                tentativas -= 1
                print(f"Erro ao buscar o álbum {album_titulo}: {e}")
                if tentativas > 0:
                    print(f"Tentando novamente ({3 - tentativas}/3)...")
                    time.sleep(5)  # Espera 5 segundos antes de tentar de novo

print(f"Os dados foram salvos em {arquivo_csv} com organização por álbuns!")
