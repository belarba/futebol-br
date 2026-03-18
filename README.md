# Brasileirao em Numeros

Analise exploratoria e estatistica do Campeonato Brasileiro de Futebol (Serie A), de 2003 a 2026, com visualizacoes interativas e modelos preditivos baseados em simulacao Monte Carlo.

## Dados

Fonte: [Kaggle - Campeonato Brasileiro de Futebol](https://www.kaggle.com/datasets/adaoduque/campeonato-brasileiro-de-futebol) + atualizacoes manuais via API.

| Arquivo | Registros | Descricao |
|---------|-----------|-----------|
| `campeonato-brasileiro-full.csv` | ~9.200 | Resultados de todas as partidas (placar, mandante, visitante, tecnico, formacao) |
| `campeonato-brasileiro-gols.csv` | ~9.800 | Detalhamento dos gols (minuto, jogador, tipo) |
| `campeonato-brasileiro-cartoes.csv` | ~20.900 | Cartoes amarelos e vermelhos por partida |
| `campeonato-brasileiro-estatisticas-full.csv` | ~17.500 | Estatisticas detalhadas por partida |

## Notebooks

| # | Notebook | Tema |
|---|----------|------|
| 01 | `exploracao` | Analise exploratoria geral — distribuicoes, medidas de tendencia central e dispersao |
| 02 | `lider_por_rodada` | Serie temporal da lideranca rodada a rodada |
| 03 | `desvio_padrao` | Variabilidade da pontuacao — coeficiente de variacao e desvio padrao |
| 04 | `mandante_visitante` | Teste de hipotese sobre vantagem do mandante |
| 05 | `gols` | Distribuicao de gols por rodada, minuto e frequencia |
| 06 | `desempenho_clubes` | Ranking historico e aproveitamento percentual |
| 07 | `turnos` | Analise comparativa entre primeiro e segundo turno |
| 08 | `rebaixamento` | Limiares de pontuacao para permanencia na Serie A |
| 09 | `pontuacao_objetivos` | Pontuacoes-alvo para titulo, Libertadores e rebaixamento |
| 10 | `gols_minuto_cartoes` | Distribuicao temporal de gols e correlacao com cartoes |
| 11 | `classicos_mandante` | Desempenho em classicos e fator casa por clube |
| 12 | `maldicao_vice_promovidos` | Analise de sobrevivencia dos recem-promovidos e desempenho do vice |
| 13 | `dia_semana_sazonalidade` | Sazonalidade e efeito do dia da semana nos resultados |
| 14 | `scatter_eficiencia` | Scatter plot de eficiencia ofensiva vs defensiva |
| 15 | `previsao_2026` | Simulacao Monte Carlo — previsao de pontuacao e classificacao final |
| 16 | `clustering_correlacao` | Clustering (K-Means) de perfis de times e matriz de correlacao |
| 17 | `previsao_evolucao` | Evolucao das probabilidades rodada a rodada via Monte Carlo |

## Graficos Interativos

49 visualizacoes interativas em Plotly, exportadas para `charts/` e acessiveis via `docs/index.html`.

**Categorias:**
- **Distribuicao e tendencia central**: boxplots de pontuacao, histogramas de gols, media movel
- **Series temporais**: evolucao de posicao, lideranca por rodada, bump charts
- **Correlacao**: heatmaps de correlacao entre variaveis, scatter de saldo vs posicao
- **Clustering**: segmentacao de perfis de times (K-Means), radar charts, scatter de clusters
- **Simulacao preditiva**: Monte Carlo com 10.000+ cenarios para classificacao 2026
- **Heatmaps**: distribuicao de gols por minuto/rodada, placares mais frequentes

## Estrutura

```
dados-futebol-br/
├── data/raw/              # CSVs com dados historicos
├── notebooks/             # 17 Jupyter notebooks de analise
├── charts/                # 49 graficos interativos (HTML/Plotly)
├── scripts/               # Scripts de coleta e build
├── docs/                  # Site estatico com todas as visualizacoes
└── requirements.txt       # Dependencias Python
```

## Como usar

```bash
pip install -r requirements.txt
jupyter notebook notebooks/
```

Para visualizar os graficos, abra `docs/index.html` no navegador.

## Tecnicas utilizadas

- Estatistica descritiva (media, mediana, desvio padrao, coeficiente de variacao)
- Testes de hipotese (vantagem do mandante)
- Simulacao Monte Carlo (previsao de classificacao)
- Clustering nao-supervisionado (K-Means)
- Analise de correlacao (Pearson)
- Series temporais e sazonalidade
- Visualizacao de dados (Plotly)
