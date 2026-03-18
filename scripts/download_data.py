"""
Download dos dados do Campeonato Brasileiro.
Fonte: https://github.com/adaoduque/Brasileirao_Dataset
"""

import os
import urllib.request

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

FILES = {
    "campeonato-brasileiro-full.csv": "https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/master/campeonato-brasileiro-full.csv",
    "campeonato-brasileiro-estatisticas-full.csv": "https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/master/campeonato-brasileiro-estatisticas-full.csv",
    "campeonato-brasileiro-gols.csv": "https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/master/campeonato-brasileiro-gols.csv",
    "campeonato-brasileiro-cartoes.csv": "https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/master/campeonato-brasileiro-cartoes.csv",
}


def download():
    os.makedirs(DATA_DIR, exist_ok=True)

    for filename, url in FILES.items():
        dest = os.path.join(DATA_DIR, filename)
        if os.path.exists(dest):
            print(f"  [skip] {filename} já existe")
            continue
        print(f"  [download] {filename} ...")
        urllib.request.urlretrieve(url, dest)
        print(f"  [ok] {filename}")

    print("\nDados salvos em:", os.path.abspath(DATA_DIR))


if __name__ == "__main__":
    print("Baixando dados do Brasileirão...\n")
    download()
