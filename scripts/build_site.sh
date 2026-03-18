#!/bin/bash
# Copia os gráficos gerados pelos notebooks para docs/charts/
# Uso: bash scripts/build_site.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

SRC="$PROJECT_DIR/charts"
DST="$PROJECT_DIR/docs/charts"

mkdir -p "$DST"

count=$(ls "$SRC"/*.html 2>/dev/null | wc -l | tr -d ' ')

if [ "$count" -eq 0 ]; then
    echo "Nenhum gráfico encontrado em $SRC"
    exit 1
fi

cp "$SRC"/*.html "$DST/"

echo "Build concluído: $count gráficos copiados para docs/charts/"
