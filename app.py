"""
Dashboard de Benchmarking de Saneamento Basico - Mato Grosso
Foco: posicionamento de Sinop (Aguas de Sinop) frente aos demais
municipios do estado, com base em indicadores do SNIS.

Indicadores utilizados:
  IN023 - Indice de atendimento urbano de agua (%)
  IN015 - Indice de coleta de esgoto (%)
  IN049 - Indice de perdas na distribuicao (%)
  FN033 - Investimentos totais realizados pelo prestador (R$)
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Configuracao geral
# ---------------------------------------------------------------------------

DATA_PATH = Path(__file__).parent / "data" / "snis_mt_2023.csv"

MUNICIPIO_DESTAQUE = "Sinop"

COR_DESTAQUE = "#E63946"   # Sinop
COR_PADRAO = "#A8DADC"     # demais municipios
COR_MEDIA = "#1D3557"      # linha de media estadual

INDICADORES = {
    "IN023": {
        "label": "IN023 - Atendimento urbano de agua (%)",
        "descricao": "Percentual da populacao urbana atendida com abastecimento de agua.",
        "melhor": "maior",
        "formato": "{:.1f}%",
    },
    "IN015": {
        "label": "IN015 - Coleta de esgoto (%)",
        "descricao": "Percentual do volume de agua consumido cujo esgoto correspondente e coletado.",
        "melhor": "maior",
        "formato": "{:.1f}%",
    },
    "IN049": {
        "label": "IN049 - Perdas na distribuicao (%)",
        "descricao": "Percentual do volume de agua produzido que e perdido (vazamentos, fraudes, erros de medicao etc.).",
        "melhor": "menor",
        "formato": "{:.1f}%",
    },
    "FN033": {
        "label": "FN033 - Investimentos totais (R$)",
        "descricao": "Investimentos totais realizados pelo prestador de servicos no ano de referencia.",
        "melhor": "maior",
        "formato": "R$ {:,.0f}",
    },
}

st.set_page_config(
    page_title="Saneamento MT - Benchmarking Sinop",
    page_icon="💧",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Carga de dados
# ---------------------------------------------------------------------------

@st.cache_data
def carregar_dados(caminho: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho)

    colunas_obrigatorias = {
        "ano",
        "codigo_ibge",
        "municipio",
        "populacao_total",
        "IN023",
        "IN015",
        "IN049",
        "FN033",
    }
    faltando = colunas_obrigatorias - set(df.columns)
    if faltando:
        raise ValueError(
            f"O arquivo de dados esta sem as colunas: {sorted(faltando)}. "
            "Verifique o README para o formato esperado."
        )

    df["fn033_per_capita"] = df["FN033"] / df["populacao_total"].replace(0, pd.NA)
    return df


if not DATA_PATH.exists():
    st.error(
        f"Arquivo de dados nao encontrado em `{DATA_PATH}`.\n\n"
        "Baixe os dados do SNIS (ver README.md) ou gere o dataset de exemplo "
        "com `python scripts/generate_sample_data.py`."
    )
    st.stop()

df = carregar_dados(DATA_PATH)

anos_disponiveis = sorted(df["ano"].unique())
ano_referencia = anos_disponiveis[-1]

df_ano = df[df["ano"] == ano_referencia].copy()

if MUNICIPIO_DESTAQUE not in df_ano["municipio"].values:
    st.warning(
        f"O municipio '{MUNICIPIO_DESTAQUE}' nao foi encontrado nos dados "
        f"para o ano {ano_referencia}. Verifique o arquivo de dados."
    )


# ---------------------------------------------------------------------------
# Sidebar - filtros
# ---------------------------------------------------------------------------

st.sidebar.title("Filtros")

if len(anos_disponiveis) > 1:
    ano_referencia = st.sidebar.selectbox(
        "Ano de referencia", anos_disponiveis, index=len(anos_disponiveis) - 1
    )
    df_ano = df[df["ano"] == ano_referencia].copy()
else:
    st.sidebar.markdown(f"**Ano de referencia:** {ano_referencia}")

municipios_ordenados = sorted(df_ano["municipio"].unique())
default_municipios = [m for m in municipios_ordenados]

municipios_selecionados = st.sidebar.multiselect(
    "Municipios para comparacao",
    options=municipios_ordenados,
    default=default_municipios,
    help=(
        f"{MUNICIPIO_DESTAQUE} e sempre incluido nos graficos e no ranking, "
        "independentemente desta selecao."
    ),
)

municipios_no_filtro = set(municipios_selecionados) | {MUNICIPIO_DESTAQUE}
df_filtro = df_ano[df_ano["municipio"].isin(municipios_no_filtro)].copy()

st.sidebar.markdown("---")
st.sidebar.caption(
    "Fonte dos dados: Sistema Nacional de Informacoes sobre Saneamento (SNIS). "
    f"{MUNICIPIO_DESTAQUE} destacado em vermelho em todos os graficos."
)


# ---------------------------------------------------------------------------
# Cabecalho e KPIs
# ---------------------------------------------------------------------------

st.title("💧 Benchmarking de Saneamento Basico - Mato Grosso")
st.markdown(
    f"Comparativo de indicadores do SNIS ({ano_referencia}) entre os municipios "
    f"de Mato Grosso, com destaque para **{MUNICIPIO_DESTAQUE}** (Aguas de Sinop)."
)

linha_sinop = df_ano[df_ano["municipio"] == MUNICIPIO_DESTAQUE]

if not linha_sinop.empty:
    sinop = linha_sinop.iloc[0]
    media_mt = df_ano[["IN023", "IN015", "IN049", "fn033_per_capita"]].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "IN023 - Atendimento de agua",
        f"{sinop['IN023']:.1f}%",
        f"{sinop['IN023'] - media_mt['IN023']:+.1f} p.p. vs media MT",
    )
    col2.metric(
        "IN015 - Coleta de esgoto",
        f"{sinop['IN015']:.1f}%",
        f"{sinop['IN015'] - media_mt['IN015']:+.1f} p.p. vs media MT",
    )
    col3.metric(
        "IN049 - Perdas na distribuicao",
        f"{sinop['IN049']:.1f}%",
        f"{sinop['IN049'] - media_mt['IN049']:+.1f} p.p. vs media MT",
        delta_color="inverse",
    )
    col4.metric(
        "Investimento per capita (FN033)",
        f"R$ {sinop['fn033_per_capita']:.2f}",
        f"R$ {sinop['fn033_per_capita'] - media_mt['fn033_per_capita']:+.2f} vs media MT",
    )

st.markdown("---")


# ---------------------------------------------------------------------------
# Funcoes auxiliares de grafico
# ---------------------------------------------------------------------------

def grafico_barras_comparativo(
    data: pd.DataFrame, coluna: str, titulo: str, eixo_y: str, formato_hover: str
) -> go.Figure:
    data = data.sort_values(coluna, ascending=False).reset_index(drop=True)
    cores = [
        COR_DESTAQUE if m == MUNICIPIO_DESTAQUE else COR_PADRAO
        for m in data["municipio"]
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=data["municipio"],
            y=data[coluna],
            marker_color=cores,
            hovertemplate="%{x}<br>" + eixo_y + ": " + formato_hover + "<extra></extra>",
        )
    )

    media = data[coluna].mean()
    fig.add_hline(
        line_dash="dash",
        line_color=COR_MEDIA,
        y=media,
        annotation_text=f"Media MT: {media:,.1f}",
        annotation_position="top left",
    )

    fig.update_layout(
        title=titulo,
        xaxis_title="Municipio",
        yaxis_title=eixo_y,
        xaxis_tickangle=-90,
        height=500,
        showlegend=False,
        margin=dict(b=150),
    )
    return fig


def calcular_ranking(df_base: pd.DataFrame, coluna: str, melhor: str) -> tuple[int, int]:
    """Retorna (posicao_de_sinop, total_de_municipios), 1 = melhor."""
    ascending = melhor == "menor"
    ordenado = df_base.sort_values(coluna, ascending=ascending).reset_index(drop=True)
    posicao = ordenado.index[ordenado["municipio"] == MUNICIPIO_DESTAQUE]
    if len(posicao) == 0:
        return (0, len(ordenado))
    return (int(posicao[0]) + 1, len(ordenado))


# ---------------------------------------------------------------------------
# Graficos principais
# ---------------------------------------------------------------------------

st.header("Cobertura de agua e esgoto")
tab_agua, tab_esgoto = st.tabs(["IN023 - Agua", "IN015 - Esgoto"])

with tab_agua:
    st.plotly_chart(
        grafico_barras_comparativo(
            df_filtro,
            "IN023",
            "Indice de atendimento urbano de agua (IN023) - Sinop vs MT",
            "IN023 (%)",
            "%{y:.1f}%",
        ),
        use_container_width=True,
    )
    st.caption(INDICADORES["IN023"]["descricao"])

with tab_esgoto:
    st.plotly_chart(
        grafico_barras_comparativo(
            df_filtro,
            "IN015",
            "Indice de coleta de esgoto (IN015) - Sinop vs MT",
            "IN015 (%)",
            "%{y:.1f}%",
        ),
        use_container_width=True,
    )
    st.caption(INDICADORES["IN015"]["descricao"])

st.markdown("---")

st.header("Indice de perdas na distribuicao de agua (IN049)")
st.plotly_chart(
    grafico_barras_comparativo(
        df_filtro,
        "IN049",
        "Indice de perdas na distribuicao (IN049) - Sinop vs MT",
        "IN049 (%)",
        "%{y:.1f}%",
    ),
    use_container_width=True,
)
st.caption(
    INDICADORES["IN049"]["descricao"]
    + " Quanto MENOR o indice, melhor a eficiencia operacional."
)

st.markdown("---")

st.header("Investimento per capita (FN033 / populacao)")
df_filtro_invest = df_filtro.dropna(subset=["fn033_per_capita"])
st.plotly_chart(
    grafico_barras_comparativo(
        df_filtro_invest,
        "fn033_per_capita",
        "Investimento total per capita - Sinop vs MT",
        "R$ por habitante",
        "R$ %{y:.2f}",
    ),
    use_container_width=True,
)
st.caption(
    "Investimentos totais realizados pelo prestador (FN033) divididos pela "
    "populacao total do municipio. Quanto MAIOR, mais recursos estao sendo "
    "investidos na infraestrutura de saneamento por habitante."
)

st.markdown("---")


# ---------------------------------------------------------------------------
# Ranking de Sinop
# ---------------------------------------------------------------------------

st.header(f"Ranking de {MUNICIPIO_DESTAQUE} entre os municipios de MT")

if linha_sinop.empty:
    st.info(f"{MUNICIPIO_DESTAQUE} nao esta presente nos dados carregados.")
else:
    linhas_ranking = []
    for codigo, info in INDICADORES.items():
        coluna = "fn033_per_capita" if codigo == "FN033" else codigo
        base_ranking = df_ano if codigo != "FN033" else df_ano.dropna(subset=["fn033_per_capita"])
        posicao, total = calcular_ranking(base_ranking, coluna, info["melhor"])
        valor_sinop = sinop[coluna]
        percentil = 100 * (total - posicao + 1) / total if total else 0

        linhas_ranking.append(
            {
                "Indicador": info["label"],
                f"Valor de {MUNICIPIO_DESTAQUE}": info["formato"].format(valor_sinop),
                "Posicao no ranking de MT": f"{posicao}º de {total}",
                "Percentil": f"Top {100 - percentil + (100/total if total else 0):.0f}%"
                if info["melhor"] == "menor"
                else f"Top {100 - percentil:.0f}%",
                "Melhor quando": "menor valor" if info["melhor"] == "menor" else "maior valor",
            }
        )

    st.dataframe(
        pd.DataFrame(linhas_ranking),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "**Como ler o ranking:** a posicao 1 representa o melhor desempenho do "
        "estado para aquele indicador (considerando a coluna 'Melhor quando'). "
        f"O percentil indica a posicao relativa de {MUNICIPIO_DESTAQUE} - por "
        "exemplo, 'Top 10%' significa que o municipio esta entre os 10% com "
        "melhor resultado em Mato Grosso."
    )


# ---------------------------------------------------------------------------
# Tabela de dados
# ---------------------------------------------------------------------------

with st.expander("Ver dados utilizados"):
    colunas_exibir = [
        "ano",
        "municipio",
        "populacao_total",
        "prestador",
        "IN023",
        "IN015",
        "IN049",
        "FN033",
        "fn033_per_capita",
    ]
    colunas_existentes = [c for c in colunas_exibir if c in df_filtro.columns]
    st.dataframe(
        df_filtro[colunas_existentes].sort_values("municipio").reset_index(drop=True),
        use_container_width=True,
    )

st.caption(
    "Dados: Sistema Nacional de Informacoes sobre Saneamento (SNIS), "
    "Ministerio das Cidades. Caso o arquivo `data/snis_mt_2023.csv` ainda "
    "contenha o dataset de EXEMPLO, substitua-o pelos dados reais antes de "
    "usar este dashboard para analises oficiais (ver README.md)."
)
