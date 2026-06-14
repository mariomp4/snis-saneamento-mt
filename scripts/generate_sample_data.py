"""
Gera um dataset de EXEMPLO (placeholder) com a mesma estrutura de colunas
esperada pelo app.py, para os 142 municipios de Mato Grosso.

IMPORTANTE: os valores dos indicadores (IN055, IN015, IN049, FN033) sao
SINTETICOS (gerados com numeros pseudoaleatorios), apenas para permitir
testar e demonstrar o dashboard antes de inserir os dados REAIS baixados
do SNIS (ver README.md - secao "Como obter os dados reais do SNIS").

A populacao de cada municipio (POPULACAO_TOTAL) e real, obtida da API do
IBGE (estimativas de populacao 2021).

Uso:
    python scripts/generate_sample_data.py
"""

import csv
import gzip
import hashlib
import json
import random
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_CSV = BASE_DIR / "data" / "snis_mt_2022.csv"

URL_MUNICIPIOS = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/MT/municipios"
URL_POPULACAO = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2021"
    "/variaveis/9324?localidades=N6[N3[51]]"
)

ANO_REFERENCIA = 2022

# Codigo IBGE do municipio que sera destacado no dashboard
CODIGO_SINOP = 5107909

# Prestadores conhecidos (apenas ilustrativo / simplificado)
PRESTADORES_CONHECIDOS = {
    5107909: "Aguas de Sinop (concessao privada)",
    5103403: "Aguas Cuiaba (concessao privada)",       # Cuiaba
    5108402: "Aguas Varzea Grande (concessao privada)",  # Varzea Grande
    5107602: "SAAER",                                   # Rondonopolis
}
PRESTADOR_PADRAO = "Autarquia / Servico Municipal (SANEMAT ou similar)"


def buscar_json(url):
    req = urllib.request.Request(url, headers={"Accept-Encoding": "identity"})
    with urllib.request.urlopen(req) as resp:
        dados = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            dados = gzip.decompress(dados)
        return json.loads(dados.decode("utf-8"))


def carregar_municipios():
    municipios = buscar_json(URL_MUNICIPIOS)
    pop_data = buscar_json(URL_POPULACAO)

    populacao_por_codigo = {}
    for serie in pop_data[0]["resultados"][0]["series"]:
        codigo = int(serie["localidade"]["id"])
        valor_bruto = list(serie["serie"].values())[0]
        try:
            valor = int(valor_bruto)
        except ValueError:
            valor = 5_000  # populacao indisponivel na API -> valor de exemplo
        populacao_por_codigo[codigo] = valor

    registros = []
    for m in municipios:
        codigo = m["id"]
        registros.append(
            {
                "codigo_ibge": codigo,
                "municipio": m["nome"],
                "populacao_total": populacao_por_codigo.get(codigo, 0),
            }
        )
    return registros


def rng_para_municipio(codigo_ibge):
    """RNG determinístico por município, para reprodutibilidade."""
    seed = int(hashlib.sha256(str(codigo_ibge).encode()).hexdigest(), 16) % (2**32)
    return random.Random(seed)


def gerar_indicadores(codigo_ibge, populacao):
    if codigo_ibge == CODIGO_SINOP:
        return {
            "IN055": 99.4,   # indice de atendimento total de agua (%)
            "IN015": 78.2,   # indice de coleta de esgoto (%)
            "IN049": 31.5,   # indice de perdas na distribuicao (%)
            "FN033": 18_500_000.0,  # investimentos totais realizados (R$)
        }

    rng = rng_para_municipio(codigo_ibge)

    # Municipios maiores tendem a ter melhor cobertura e menores perdas
    porte = min(max((populacao - 2_000) / 150_000, 0), 1)  # 0 (pequeno) .. 1 (grande)

    in055 = 70 + porte * 25 + rng.gauss(0, 8)
    in055 = min(max(in055, 35), 100)

    in015 = 10 + porte * 55 + rng.gauss(0, 12)
    in015 = min(max(in015, 0), 95)

    in049 = 50 - porte * 12 + rng.gauss(0, 10)
    in049 = min(max(in049, 15), 75)

    investimento_per_capita = max(rng.gauss(25, 15), 0)
    fn033 = investimento_per_capita * populacao

    return {
        "IN055": round(in055, 1),
        "IN015": round(in015, 1),
        "IN049": round(in049, 1),
        "FN033": round(fn033, 2),
    }


def main():
    registros = carregar_municipios()
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "ano",
                "codigo_ibge",
                "municipio",
                "populacao_total",
                "prestador",
                "IN055",
                "IN015",
                "IN049",
                "FN033",
            ]
        )
        for reg in registros:
            codigo = reg["codigo_ibge"]
            populacao = reg["populacao_total"]
            indicadores = gerar_indicadores(codigo, populacao)
            prestador = PRESTADORES_CONHECIDOS.get(codigo, PRESTADOR_PADRAO)
            writer.writerow(
                [
                    ANO_REFERENCIA,
                    codigo,
                    reg["municipio"],
                    populacao,
                    prestador,
                    indicadores["IN055"],
                    indicadores["IN015"],
                    indicadores["IN049"],
                    indicadores["FN033"],
                ]
            )

    print(f"Arquivo gerado: {OUTPUT_CSV} ({len(registros)} municipios)")


if __name__ == "__main__":
    main()
