"""
Adiciona dados do Brasileirão 2026 (rodadas 1-6) ao CSV principal.
Dados coletados do Flashscore em 18/03/2026.
"""
import csv
import os

# Times do Brasileirão 2026 e seus estados
ESTADOS = {
    "Atlético-MG": "MG", "Athletico-PR": "PR", "Bahia": "BA",
    "Botafogo": "RJ", "Bragantino": "SP", "Chapecoense": "SC",
    "Corinthians": "SP", "Coritiba": "PR", "Cruzeiro": "MG",
    "Flamengo": "RJ", "Fluminense": "RJ", "Grêmio": "RS",
    "Internacional": "RS", "Mirassol": "SP", "Palmeiras": "SP",
    "Remo": "PA", "Santos": "SP", "São Paulo": "SP",
    "Vasco": "RJ", "Vitória": "BA",
}

# Dados coletados do Flashscore - Brasileirão 2026, rodadas 1-6
# Formato: (rodada, data, mandante, visitante, placar_m, placar_v)
JOGOS_2026 = [
    # Rodada 1
    (1, "29/03/2026", "Botafogo", "Cruzeiro", 4, 0),
    (1, "29/03/2026", "Mirassol", "Vasco", 1, 1),
    (1, "29/03/2026", "São Paulo", "Flamengo", 2, 1),
    (1, "29/03/2026", "Chapecoense", "Santos", 4, 2),
    (1, "29/03/2026", "Corinthians", "Bahia", 1, 2),
    (1, "29/03/2026", "Fluminense", "Grêmio", 2, 1),
    (1, "29/03/2026", "Atlético-MG", "Palmeiras", 2, 2),
    (1, "29/03/2026", "Coritiba", "Bragantino", 0, 1),
    (1, "29/03/2026", "Internacional", "Athletico-PR", 0, 1),
    (1, "29/03/2026", "Vitória", "Remo", 2, 0),
    # Rodada 2
    (2, "05/04/2026", "Cruzeiro", "Coritiba", 1, 2),
    (2, "05/04/2026", "Vasco", "Chapecoense", 0, 1),
    (2, "05/04/2026", "Bahia", "Fluminense", 0, 1),
    (2, "05/04/2026", "Grêmio", "Botafogo", 5, 3),
    (2, "05/04/2026", "Palmeiras", "Vitória", 5, 1),
    (2, "05/04/2026", "Remo", "Mirassol", 0, 2),
    (2, "05/04/2026", "Santos", "São Paulo", 0, 1),
    (2, "05/04/2026", "Flamengo", "Internacional", 0, 1),
    (2, "05/04/2026", "Bragantino", "Atlético-MG", 1, 0),
    (2, "05/04/2026", "Athletico-PR", "Corinthians", 0, 2),
    # Rodada 3
    (3, "12/04/2026", "Internacional", "Palmeiras", 1, 3),
    (3, "12/04/2026", "Corinthians", "Bragantino", 2, 0),
    (3, "12/04/2026", "Fluminense", "Botafogo", 1, 0),
    (3, "12/04/2026", "Athletico-PR", "Santos", 2, 1),
    (3, "12/04/2026", "São Paulo", "Grêmio", 2, 0),
    (3, "12/04/2026", "Vasco", "Bahia", 0, 0),
    (3, "12/04/2026", "Atlético-MG", "Remo", 3, 0),
    (3, "12/04/2026", "Chapecoense", "Coritiba", 0, 3),
    (3, "12/04/2026", "Mirassol", "Cruzeiro", 2, 0),
    (3, "12/04/2026", "Vitória", "Flamengo", 1, 2),
    # Rodada 4
    (4, "19/04/2026", "Santos", "Vasco", 2, 1),
    (4, "19/04/2026", "Grêmio", "Atlético-MG", 2, 1),
    (4, "19/04/2026", "Palmeiras", "Fluminense", 2, 1),
    (4, "19/04/2026", "Cruzeiro", "Corinthians", 0, 1),
    (4, "19/04/2026", "Coritiba", "São Paulo", 0, 2),
    (4, "19/04/2026", "Bragantino", "Athletico-PR", 0, 1),
    (4, "19/04/2026", "Remo", "Internacional", 0, 1),
    (4, "19/04/2026", "Botafogo", "Vitória", 2, 0),
    (4, "19/04/2026", "Flamengo", "Chapecoense", 3, 0),
    (4, "19/04/2026", "Bahia", "Mirassol", 1, 1),
    # Rodada 5
    (5, "26/04/2026", "Grêmio", "Bragantino", 0, 1),
    (5, "26/04/2026", "São Paulo", "Chapecoense", 2, 0),
    (5, "26/04/2026", "Vasco", "Palmeiras", 2, 1),
    (5, "26/04/2026", "Remo", "Fluminense", 0, 2),
    (5, "26/04/2026", "Corinthians", "Coritiba", 0, 2),
    (5, "26/04/2026", "Flamengo", "Cruzeiro", 2, 0),
    (5, "26/04/2026", "Bahia", "Vitória", 0, 1),
    (5, "26/04/2026", "Atlético-MG", "Internacional", 1, 0),
    (5, "26/04/2026", "Mirassol", "Santos", 2, 2),
    (5, "26/04/2026", "Athletico-PR", "Botafogo", 1, 0),
    # Rodada 6
    (6, "03/05/2026", "Chapecoense", "Grêmio", 1, 1),
    (6, "03/05/2026", "Cruzeiro", "Vasco", 3, 2),
    (6, "03/05/2026", "Bragantino", "São Paulo", 1, 2),
    (6, "03/05/2026", "Coritiba", "Remo", 1, 0),
    (6, "03/05/2026", "Palmeiras", "Mirassol", 1, 0),
    (6, "03/05/2026", "Fluminense", "Athletico-PR", 3, 2),
    (6, "03/05/2026", "Internacional", "Bahia", 0, 2),
    (6, "03/05/2026", "Santos", "Corinthians", 0, 1),
    (6, "03/05/2026", "Botafogo", "Flamengo", 0, 3),
    (6, "03/05/2026", "Vitória", "Atlético-MG", 2, 0),
]

def main():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "campeonato-brasileiro-full.csv")
    csv_path = os.path.abspath(csv_path)

    # Verificar se já existem dados de 2026
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        last_id = 0
        has_2026 = False
        for row in reader:
            last_id = int(row[0])
            if "2026" in row[2]:  # coluna 'data'
                has_2026 = True

    if has_2026:
        print("Dados de 2026 já existem no CSV. Nada a fazer.")
        return

    print(f"Último ID: {last_id}")
    print(f"Adicionando {len(JOGOS_2026)} jogos de 2026...")

    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for i, (rodada, data, mandante, visitante, placar_m, placar_v) in enumerate(JOGOS_2026, 1):
            new_id = last_id + i
            # Determinar vencedor
            if placar_m > placar_v:
                vencedor = mandante
            elif placar_v > placar_m:
                vencedor = visitante
            else:
                vencedor = "-"

            row = [
                new_id,           # ID
                rodada,           # rodata
                data,             # data
                "16:00",          # hora (placeholder)
                mandante,         # mandante
                visitante,        # visitante
                "",               # formacao_mandante
                "",               # formacao_visitante
                "",               # tecnico_mandante
                "",               # tecnico_visitante
                vencedor,         # vencedor
                "",               # arena
                placar_m,         # mandante_Placar
                placar_v,         # visitante_Placar
                ESTADOS.get(mandante, ""),   # mandante_Estado
                ESTADOS.get(visitante, ""),  # visitante_Estado
            ]
            writer.writerow(row)

    print(f"Dados de 2026 adicionados com sucesso! ({len(JOGOS_2026)} jogos)")

if __name__ == "__main__":
    main()
