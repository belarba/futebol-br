"""
Adiciona dados do Brasileirão 2025 ao CSV principal.
Usa a tabela de confrontos (resultados) + arquivo xlsb (rodadas/datas).
"""
import csv
import os
import sys
from datetime import datetime, timedelta

import pandas as pd

# Tabela de confrontos 2025 - Mandante (linha) x Visitante (coluna)
# Formato: "gols_mandante-gols_visitante"
TEAMS = [
    "Atlético-MG", "Bahia", "Botafogo", "Ceará", "Corinthians",
    "Cruzeiro", "Flamengo", "Fluminense", "Fortaleza", "Grêmio",
    "Internacional", "Juventude", "Mirassol", "Palmeiras",
    "Bragantino", "Santos", "São Paulo", "Sport", "Vasco", "Vitória",
]

# Nomes no xlsb -> nomes no CSV
XLSB_TO_CSV = {
    "Atlético/MG": "Atlético-MG",
    "RB Bragantino": "Bragantino",
    "Red Bull Bragantino": "Bragantino",
    "Vasco da Gama": "Vasco",
    "Vasco Da Gama": "Vasco",
}

ESTADOS = {
    "Atlético-MG": "MG", "Bahia": "BA", "Botafogo": "RJ", "Ceará": "CE",
    "Corinthians": "SP", "Cruzeiro": "MG", "Flamengo": "RJ",
    "Fluminense": "RJ", "Fortaleza": "CE", "Grêmio": "RS",
    "Internacional": "RS", "Juventude": "RS", "Mirassol": "SP",
    "Palmeiras": "SP", "Bragantino": "SP", "Santos": "SP",
    "São Paulo": "SP", "Sport": "PE", "Vasco": "RJ", "Vitória": "BA",
}

# Matriz de confrontos: CONFRONTOS[i][j] = "gm-gv" quando TEAMS[i] joga em casa contra TEAMS[j]
CONFRONTOS = [
    # ATM   BAH   BOT   CEA   COR   CRU   FLA   FLU   FOR   GRE   INT   JUV   MIR   PAL   RBB   SAN   SPA   SPT   VAS   VIT
    [None, "3-0","1-0","1-0","0-0","1-1","1-1","3-2","3-3","1-3","2-0","0-0","1-0","0-3","1-3","1-0","0-0","3-1","5-0","2-2"],  # Atlético-MG
    ["2-1",None, "1-0","1-0","1-1","1-2","1-0","3-3","2-3","4-0","1-0","3-0","1-1","1-0","2-1","2-0","2-1","2-0","1-0","2-1"],  # Bahia
    ["1-0","2-1",None, "3-2","1-1","0-2","0-3","2-0","4-2","3-2","4-0","2-0","3-3","0-1","4-1","2-2","2-2","3-2","3-0","0-0"],  # Botafogo
    ["0-1","1-1","0-2",None, "0-1","1-1","1-1","2-0","1-1","2-0","1-2","1-2","0-2","1-3","1-0","3-0","1-1","2-0","2-1","1-0"],  # Ceará
    ["1-0","1-2","2-2","0-1",None, "0-0","1-2","0-2","1-1","2-0","4-2","1-1","3-0","1-1","1-2","1-0","3-1","2-1","3-0","0-0"],  # Corinthians
    ["0-0","3-0","2-2","1-2","3-0",None, "2-1","0-0","1-0","4-1","2-1","4-0","2-1","2-1","2-1","1-2","1-0","1-1","1-0","3-1"],  # Cruzeiro
    ["1-0","1-0","0-0","1-0","4-0","0-0",None, "1-0","5-0","1-1","1-1","6-0","2-1","3-2","3-0","3-2","2-0","3-0","1-1","8-0"],  # Flamengo
    ["3-0","2-0","2-0","1-0","0-1","0-2","2-1",None, "2-1","1-0","1-0","1-0","1-0","1-2","2-1","1-0","6-0","2-1","2-1","1-1"],  # Fluminense
    ["1-0","1-1","0-5","0-1","2-1","0-2","1-0","2-0",None, "2-2","0-0","5-0","0-1","1-2","3-1","2-3","0-2","1-0","0-2","2-0"],  # Fortaleza
    ["2-1","1-0","1-1","0-0","1-1","0-1","0-2","1-2","2-1",None, "1-1","3-1","0-1","3-2","1-1","1-0","2-0","0-1","2-0","3-1"],  # Grêmio
    ["0-0","2-2","2-0","1-0","1-1","3-0","1-3","0-2","2-1","2-3",None, "3-1","1-1","0-1","3-1","1-1","1-2","2-0","1-1","1-0"],  # Internacional
    ["0-1","1-1","1-3","2-1","2-1","3-3","0-2","1-1","1-2","0-2","1-1",None, "2-2","0-2","1-0","0-3","0-1","2-0","2-0","2-0"],  # Juventude
    ["2-2","5-1","0-0","3-0","2-1","1-1","3-3","2-1","1-1","4-1","3-1","2-0",None, "2-1","1-1","3-0","3-0","1-0","3-2","1-1"],  # Mirassol
    ["3-2","0-1","0-0","2-1","2-0","0-0","0-2","0-0","4-1","1-0","4-1","4-1","1-1",None, "5-1","2-0","1-0","3-0","3-0","0-0"],  # Palmeiras
    ["2-0","0-3","1-0","2-2","2-1","1-0","1-2","4-2","0-1","1-0","1-3","1-0","1-0","1-2",None, "2-2","2-2","1-1","0-3","4-0"],  # Bragantino
    ["2-0","2-2","0-1","0-0","3-1","3-0","1-0","0-0","1-1","1-1","1-2","3-1","1-1","1-0","1-2",None, "1-0","3-0","0-6","0-1"],  # Santos
    ["2-0","2-0","1-0","0-1","2-0","1-1","2-2","3-1","0-0","2-1","3-0","2-1","0-2","2-3","0-1","2-1",None, "0-0","1-3","2-0"],  # São Paulo
    ["2-4","0-0","0-1","1-1","1-0","0-4","1-5","2-2","0-0","0-4","1-1","0-2","1-2","1-2","0-1","2-2","2-2",None, "2-3","1-3"],  # Sport
    ["1-1","3-1","0-2","2-2","2-3","2-0","0-0","2-0","3-0","1-1","5-1","1-3","0-2","0-1","0-2","2-1","0-2","3-1",None, "4-3"],  # Vasco
    ["1-0","2-1","0-0","1-0","0-1","0-0","1-2","0-1","2-1","1-1","1-0","2-2","2-0","2-2","1-0","0-1","1-0","2-2","2-1",None],  # Vitória
]


def normalize_team(name):
    """Normaliza nome do time."""
    name = name.strip()
    return XLSB_TO_CSV.get(name, name)


def excel_date_to_str(excel_date):
    """Converte número serial do Excel para DD/MM/YYYY."""
    if pd.isna(excel_date):
        return ""
    # Excel date serial: days since 1899-12-30
    base = datetime(1899, 12, 30)
    dt = base + timedelta(days=int(excel_date))
    return dt.strftime("%d/%m/%Y")


def excel_time_to_str(excel_time):
    """Converte fração do dia para HH:MM."""
    if pd.isna(excel_time):
        return "16:00"
    total_minutes = int(float(excel_time) * 24 * 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"


def get_score(mandante, visitante):
    """Busca o placar na tabela de confrontos."""
    try:
        i = TEAMS.index(mandante)
        j = TEAMS.index(visitante)
    except ValueError:
        return None, None

    result = CONFRONTOS[i][j]
    if result is None:
        return None, None

    parts = result.split("-")
    return int(parts[0]), int(parts[1])


def read_schedule_from_xlsb():
    """Lê o calendário do arquivo xlsb."""
    xlsb_path = "/Users/danielsilva/Downloads/BRASILEIRAO SERIE A 2025 - GRÁTIS.xlsb"
    if not os.path.exists(xlsb_path):
        print(f"Erro: arquivo não encontrado: {xlsb_path}")
        sys.exit(1)

    df = pd.read_excel(xlsb_path, engine="pyxlsb", sheet_name="Jogos", header=None)

    schedule = []
    current_rodada = 0

    for idx in range(5, len(df)):
        row = df.iloc[idx]

        # Coluna 1: rodada (ex: "1ª", "2ª")
        if pd.notna(row[1]) and isinstance(row[1], str) and "ª" in str(row[1]):
            current_rodada = int(str(row[1]).replace("ª", ""))

        # Coluna 4: mandante
        mandante = row[4] if pd.notna(row[4]) else None
        if mandante is None:
            continue

        mandante = normalize_team(str(mandante))
        visitante = normalize_team(str(row[8])) if pd.notna(row[8]) else ""
        data = excel_date_to_str(row[2])
        hora = excel_time_to_str(row[3])
        estadio = str(row[9]) if pd.notna(row[9]) else ""

        if mandante and visitante and current_rodada > 0:
            schedule.append({
                "rodada": current_rodada,
                "data": data,
                "hora": hora,
                "mandante": mandante,
                "visitante": visitante,
                "arena": estadio,
            })

    return schedule


def main():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "campeonato-brasileiro-full.csv")
    csv_path = os.path.abspath(csv_path)

    # Verificar se já existem dados de 2025
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # header
        has_2025 = False
        for row in reader:
            if "/2025" in row[2]:
                has_2025 = True
                break

    if has_2025:
        print("Dados de 2025 já existem no CSV. Nada a fazer.")
        return

    # Ler calendário do xlsb
    print("Lendo calendário do xlsb...")
    schedule = read_schedule_from_xlsb()
    print(f"Jogos no calendário: {len(schedule)}")

    # Combinar com placares da tabela de confrontos
    matches = []
    missing = []
    for game in schedule:
        gm, gv = get_score(game["mandante"], game["visitante"])
        if gm is None:
            missing.append(f"  {game['mandante']} vs {game['visitante']}")
            continue

        if gm > gv:
            vencedor = game["mandante"]
        elif gv > gm:
            vencedor = game["visitante"]
        else:
            vencedor = "-"

        matches.append({
            **game,
            "mandante_Placar": gm,
            "visitante_Placar": gv,
            "vencedor": vencedor,
            "mandante_Estado": ESTADOS.get(game["mandante"], ""),
            "visitante_Estado": ESTADOS.get(game["visitante"], ""),
        })

    print(f"Jogos com placar: {len(matches)}")
    if missing:
        print(f"Jogos sem placar ({len(missing)}):")
        for m in missing[:5]:
            print(m)

    if len(matches) != 380:
        print(f"AVISO: esperados 380 jogos, encontrados {len(matches)}")

    # Ler CSV existente
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        all_rows = list(reader)

    # Separar pré-2026 e 2026
    rows_pre2026 = [r for r in all_rows if "/2026" not in r[2]]
    rows_2026 = [r for r in all_rows if "/2026" in r[2]]

    last_pre2026_id = int(rows_pre2026[-1][0]) if rows_pre2026 else 0

    # Criar linhas para 2025
    new_rows = []
    for i, m in enumerate(matches, 1):
        new_rows.append([
            last_pre2026_id + i,  # ID
            m["rodada"],
            m["data"],
            m["hora"],
            m["mandante"],
            m["visitante"],
            "",  # formacao_mandante
            "",  # formacao_visitante
            "",  # tecnico_mandante
            "",  # tecnico_visitante
            m["vencedor"],
            m["arena"],
            m["mandante_Placar"],
            m["visitante_Placar"],
            m["mandante_Estado"],
            m["visitante_Estado"],
        ])

    # Renumerar IDs de 2026
    next_id = last_pre2026_id + len(new_rows) + 1
    for row in rows_2026:
        row[0] = str(next_id)
        next_id += 1

    # Reescrever CSV
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
    print(f"  Jogos até 2024: {len(rows_pre2026)}")
    print(f"  Jogos 2025: {len(new_rows)}")
    print(f"  Jogos 2026: {len(rows_2026)}")
    print(f"  Total: {total}")

    # Amostra
    print("\nAmostra:")
    for r in new_rows[:3]:
        print(f"  R{r[1]}: {r[4]} {r[12]}x{r[13]} {r[5]} ({r[2]})")
    print("  ...")
    for r in new_rows[-3:]:
        print(f"  R{r[1]}: {r[4]} {r[12]}x{r[13]} {r[5]} ({r[2]})")


if __name__ == "__main__":
    main()
