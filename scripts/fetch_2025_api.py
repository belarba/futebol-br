"""
Busca todos os jogos do Brasileirão 2025 via API-Football (api-sports.io)
e adiciona ao CSV principal.

Uso: python3 scripts/fetch_2025_api.py
Requer: .env com API_FOOTBALL_KEY=<sua_chave>
"""
import csv
import json
import os
import sys
import time
import urllib.request

# Carregar .env manualmente (sem dependência de python-dotenv)
def load_env(path=".env"):
    if not os.path.exists(path):
        print(f"Erro: arquivo {path} não encontrado. Crie com API_FOOTBALL_KEY=<sua_chave>")
        sys.exit(1)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

load_env()

API_KEY = os.environ.get("API_FOOTBALL_KEY")
if not API_KEY:
    print("Erro: API_FOOTBALL_KEY não encontrada no .env")
    sys.exit(1)

BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io",
}

ESTADOS = {
    "Atletico Mineiro": "MG", "Atletico-MG": "MG", "Atlético-MG": "MG", "Atlético Mineiro": "MG",
    "Athletico Paranaense": "PR", "Athletico-PR": "PR",
    "Bahia": "BA",
    "Botafogo": "RJ",
    "Red Bull Bragantino": "SP", "Bragantino": "SP",
    "Ceará": "CE", "Ceara": "CE",
    "Chapecoense": "SC",
    "Corinthians": "SP",
    "Coritiba": "PR",
    "Criciuma": "SC", "Criciúma": "SC",
    "Cruzeiro": "MG",
    "Cuiaba": "MT", "Cuiabá": "MT",
    "Flamengo": "RJ",
    "Fluminense": "RJ",
    "Fortaleza": "CE",
    "Goias": "GO", "Goiás": "GO",
    "Gremio": "RS", "Grêmio": "RS",
    "Internacional": "RS",
    "Juventude": "RS",
    "Mirassol": "SP",
    "Palmeiras": "SP",
    "Remo": "PA",
    "Santos": "SP",
    "Sao Paulo": "SP", "São Paulo": "SP",
    "Sport Recife": "PE", "Sport": "PE",
    "Vasco DA Gama": "RJ", "Vasco da Gama": "RJ", "Vasco": "RJ",
    "Vitoria": "BA", "Vitória": "BA",
}

# Mapeamento de nomes da API para nomes do CSV
NOME_CSV = {
    "Atletico-MG": "Atlético-MG",
    "Atletico Mineiro": "Atlético-MG",
    "Atlético Mineiro": "Atlético-MG",
    "Athletico Paranaense": "Athletico-PR",
    "Red Bull Bragantino": "Bragantino",
    "Vasco DA Gama": "Vasco",
    "Vasco da Gama": "Vasco",
    "Sport Recife": "Sport",
    "Sao Paulo": "São Paulo",
    "Ceara": "Ceará",
    "Cuiaba": "Cuiabá",
    "Goias": "Goiás",
    "Gremio": "Grêmio",
    "Criciuma": "Criciúma",
    "Vitoria": "Vitória",
}


def api_request(endpoint, params=None):
    """Faz uma requisição à API-Football."""
    url = f"{BASE_URL}/{endpoint}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"

    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())

    # Mostrar limites de uso
    if "errors" in data and data["errors"]:
        print(f"API Errors: {data['errors']}")

    return data


def find_league_id():
    """Encontra o ID da liga Brasileirão Série A."""
    data = api_request("leagues", {"country": "Brazil", "season": "2025", "type": "league"})
    for league in data.get("response", []):
        name = league["league"]["name"]
        if "Serie A" in name or "Série A" in name:
            lid = league["league"]["id"]
            print(f"Liga encontrada: {name} (ID: {lid})")
            return lid
    print("Liga não encontrada! Tentando ID 71 (padrão para Série A)...")
    return 71


def normalizar_nome(nome):
    """Normaliza nome do time para o padrão do CSV."""
    return NOME_CSV.get(nome, nome)


def get_estado(nome):
    """Retorna o estado do time."""
    for key, val in ESTADOS.items():
        if key in nome or nome in key:
            return val
    return ""


def fetch_fixtures(league_id, season):
    """Busca todos os jogos finalizados de uma temporada."""
    print(f"\nBuscando jogos da temporada {season}...")
    data = api_request("fixtures", {
        "league": league_id,
        "season": season,
        "status": "FT-AET-PEN",
    })

    fixtures = data.get("response", [])
    print(f"Total de jogos encontrados: {len(fixtures)}")
    return fixtures


def fixture_to_row(fixture, next_id):
    """Converte um fixture da API para uma linha do CSV."""
    league_round = fixture["league"].get("round", "")
    # Extrair número da rodada: "Regular Season - 1" -> 1
    rodada = ""
    if "Regular Season" in league_round:
        rodada = league_round.split(" - ")[-1]

    # Data: "2025-04-12T20:00:00+00:00" -> "12/04/2025"
    date_str = fixture["fixture"]["date"][:10]  # "2025-04-12"
    parts = date_str.split("-")
    data = f"{parts[2]}/{parts[1]}/{parts[0]}"

    # Hora
    hora = fixture["fixture"]["date"][11:16]  # "20:00"

    mandante = normalizar_nome(fixture["teams"]["home"]["name"])
    visitante = normalizar_nome(fixture["teams"]["away"]["name"])
    gols_m = fixture["goals"]["home"]
    gols_v = fixture["goals"]["away"]

    if gols_m is None or gols_v is None:
        return None

    if gols_m > gols_v:
        vencedor = mandante
    elif gols_v > gols_m:
        vencedor = visitante
    else:
        vencedor = "-"

    arena = fixture["fixture"]["venue"]["name"] or ""

    return [
        next_id,
        rodada,
        data,
        hora,
        mandante,
        visitante,
        "",  # formacao_mandante
        "",  # formacao_visitante
        "",  # tecnico_mandante
        "",  # tecnico_visitante
        vencedor,
        arena,
        gols_m,
        gols_v,
        get_estado(mandante),
        get_estado(visitante),
    ]


def main():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "campeonato-brasileiro-full.csv")
    csv_path = os.path.abspath(csv_path)

    # Verificar se já existem dados de 2025
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # header
        last_id = 0
        has_2025 = False
        for row in reader:
            last_id = int(row[0])
            if "/2025" in row[2]:
                has_2025 = True

    if has_2025:
        print("Dados de 2025 já existem no CSV. Nada a fazer.")
        return

    # Encontrar league ID
    league_id = find_league_id()
    time.sleep(1)  # Rate limit

    # Buscar fixtures
    fixtures = fetch_fixtures(league_id, 2025)

    if not fixtures:
        print("Nenhum jogo encontrado!")
        return

    # Ordenar por rodada e data
    def sort_key(f):
        r = f["league"].get("round", "")
        rod = int(r.split(" - ")[-1]) if "Regular Season" in r else 0
        return (rod, f["fixture"]["date"])

    fixtures.sort(key=sort_key)

    # Precisamos inserir ANTES dos dados de 2026
    # Ler todo o CSV
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        all_rows = list(reader)

    # Separar dados pré-2026 e 2026
    rows_pre2026 = [r for r in all_rows if "/2026" not in r[2]]
    rows_2026 = [r for r in all_rows if "/2026" in r[2]]

    last_pre2026_id = int(rows_pre2026[-1][0]) if rows_pre2026 else 0

    # Converter fixtures para linhas
    new_rows = []
    for i, fixture in enumerate(fixtures, 1):
        row = fixture_to_row(fixture, last_pre2026_id + i)
        if row:
            new_rows.append(row)

    print(f"\nConvertidos {len(new_rows)} jogos para o formato CSV")

    # Mostrar amostra
    print("\nAmostra dos primeiros jogos:")
    for row in new_rows[:3]:
        print(f"  R{row[1]}: {row[4]} {row[12]}x{row[13]} {row[5]} ({row[2]})")

    # Renumerar IDs dos dados de 2026
    next_id = last_pre2026_id + len(new_rows) + 1
    for row in rows_2026:
        row[0] = str(next_id)
        next_id += 1

    # Reescrever CSV completo
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for row in rows_pre2026:
            writer.writerow(row)
        for row in new_rows:
            writer.writerow(row)
        for row in rows_2026:
            writer.writerow(row)

    total = len(rows_pre2026) + len(new_rows) + len(rows_2026)
    print(f"\nCSV atualizado com sucesso!")
    print(f"  Jogos pré-2025: {len(rows_pre2026)}")
    print(f"  Jogos 2025: {len(new_rows)}")
    print(f"  Jogos 2026: {len(rows_2026)}")
    print(f"  Total: {total}")


if __name__ == "__main__":
    main()
