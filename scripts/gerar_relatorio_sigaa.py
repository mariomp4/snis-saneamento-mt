"""Gera o relatorio tecnico do projeto (PDF) para envio no SIGAA."""

from datetime import date
from fpdf import FPDF

OUTPUT_PATH = "relatorio_sigaa.pdf"

INSTITUICAO = "Universidade do Estado de Mato Grosso (UNEMAT)"
FACULDADE = "Faculdade Carlos Alberto Reyes Maldonado"
CURSO = "Ciências Econômicas"
DISCIPLINA = "Ciência de Dados para Economistas"
PROFESSOR = "Feliciano Lhanos Azuaga"
DOCENTE = "Mario Garcia Filho"
TITULO = "Dashboard de Benchmarking de Saneamento Básico em Mato Grosso: o Posicionamento de Sinop"


class Relatorio(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, TITULO, align="L")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def titulo_secao(self, texto, numero=None):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 0, 0)
        prefixo = f"{numero}. " if numero else ""
        self.cell(0, 10, prefixo + texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def subtitulo(self, texto):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, texto, new_x="LMARGIN", new_y="NEXT")

    def paragrafo(self, texto):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def item_lista(self, texto):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin + 5)
        self.multi_cell(0, 6, f"- {texto}", new_x="LMARGIN", new_y="NEXT")

    def tabela_indicadores(self, linhas):
        for codigo, indicador, descricao in linhas:
            self.set_x(self.l_margin)
            self.set_font("Helvetica", "B", 11)
            self.multi_cell(
                0, 6, f"{codigo} - {indicador}", new_x="LMARGIN", new_y="NEXT"
            )
            self.set_x(self.l_margin + 5)
            self.set_font("Helvetica", "", 10)
            self.multi_cell(0, 6, descricao, new_x="LMARGIN", new_y="NEXT")
            self.ln(1)
        self.ln(1)


pdf = Relatorio(format="A4")
pdf.set_auto_page_break(auto=True, margin=20)
pdf.set_margins(20, 20, 20)
pdf.alias_nb_pages()

# ---------------------------------------------------------------------------
# Capa
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_font("Helvetica", "B", 13)
pdf.ln(15)
pdf.set_x(pdf.l_margin)
pdf.multi_cell(0, 8, INSTITUICAO, align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 12)
pdf.set_x(pdf.l_margin)
pdf.multi_cell(0, 7, FACULDADE, align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_x(pdf.l_margin)
pdf.multi_cell(0, 7, f"Curso: {CURSO}", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(pdf.l_margin)
pdf.multi_cell(0, 7, f"Disciplina: {DISCIPLINA}", align="C", new_x="LMARGIN", new_y="NEXT")

pdf.ln(60)
pdf.set_font("Helvetica", "B", 16)
pdf.set_x(pdf.l_margin)
pdf.multi_cell(0, 9, TITULO, align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 12)
pdf.ln(2)
pdf.set_x(pdf.l_margin)
pdf.multi_cell(0, 7, "Relatório Técnico de Projeto", align="C", new_x="LMARGIN", new_y="NEXT")

pdf.ln(60)
pdf.set_font("Helvetica", "", 12)
pdf.cell(0, 7, f"Docente: {DOCENTE}", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.cell(0, 7, f"Professor da disciplina: {PROFESSOR}", new_x="LMARGIN", new_y="NEXT", align="C")

pdf.ln(20)
hoje = date.today()
meses = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
]
data_extenso = f"{hoje.day} de {meses[hoje.month - 1]} de {hoje.year}"
pdf.set_x(pdf.l_margin)
pdf.cell(0, 7, f"Sinop/MT, {data_extenso}", align="C")

# ---------------------------------------------------------------------------
# 1. Introdução
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.titulo_secao("Introdução", 1)
pdf.paragrafo(
    "O saneamento básico é um dos determinantes mais importantes da qualidade "
    "de vida, da saúde pública e do desenvolvimento econômico de uma região. "
    "No Brasil, o Sistema Nacional de Informações sobre Saneamento (SNIS), "
    "mantido pelo Ministério das Cidades, consolida anualmente indicadores de "
    "abastecimento de água, esgotamento sanitário, perdas na distribuição e "
    "investimentos realizados pelos prestadores de serviço em todos os "
    "municípios brasileiros."
)
pdf.paragrafo(
    "Este projeto consiste no desenvolvimento de um dashboard interativo, "
    "construído em Python com a biblioteca Streamlit, que permite comparar "
    "indicadores de saneamento básico dos municípios do estado de Mato "
    "Grosso com dados completos no Diagnóstico SNIS 2022 (40 dos 142 "
    "municípios do estado), com destaque para o posicionamento do município "
    "de Sinop (operado pela concessionária Águas de Sinop) frente aos demais "
    "municípios."
)

# ---------------------------------------------------------------------------
# 2. Objetivos
# ---------------------------------------------------------------------------
pdf.titulo_secao("Objetivos", 2)
pdf.subtitulo("2.1 Objetivo Geral")
pdf.paragrafo(
    "Desenvolver uma ferramenta de visualização e análise de dados que "
    "permita avaliar, de forma comparativa, o desempenho dos indicadores de "
    "saneamento básico dos municípios de Mato Grosso, com foco no "
    "benchmarking do município de Sinop."
)
pdf.subtitulo("2.2 Objetivos Específicos")
for item in [
    "Coletar e tratar dados oficiais do SNIS referentes aos municípios de Mato Grosso;",
    "Calcular e comparar indicadores de cobertura de água, coleta de esgoto, "
    "perdas na distribuição e investimento per capita;",
    "Construir visualizações gráficas interativas (gráficos de barras e "
    "tabelas) que destaquem a posição de Sinop em relação aos demais "
    "municípios;",
    "Apresentar o ranking percentual de Sinop para cada indicador analisado;",
    "Disponibilizar o dashboard de forma acessível, com filtros dinâmicos "
    "por município.",
]:
    pdf.item_lista(item)
pdf.ln(2)

# ---------------------------------------------------------------------------
# 3. Base de Dados e Metodologia
# ---------------------------------------------------------------------------
pdf.titulo_secao("Base de Dados e Metodologia", 3)
pdf.paragrafo(
    "Os dados utilizados têm como fonte o SNIS (Sistema Nacional de "
    "Informações sobre Saneamento), por meio da consulta de Informações "
    "Desagregadas por Município, considerando a abrangência do estado de "
    "Mato Grosso (MT) e o Diagnóstico 2022 (último ano-base com dados "
    "completos para os indicadores analisados). Dos 142 municípios de MT, "
    "40 possuíam os quatro indicadores informados no SNIS 2022. A lista de "
    "municípios e suas respectivas populações foram obtidas a partir da API "
    "pública do IBGE (estimativas 2021)."
)
pdf.paragrafo("Os quatro indicadores centrais da análise são:")
pdf.tabela_indicadores([
    ("IN055", "Índice de atendimento total de água",
     "Percentual da população total (urbana + rural) atendida com abastecimento de água."),
    ("IN015", "Índice de coleta de esgoto",
     "Percentual do volume de água consumido cujo esgoto correspondente é coletado."),
    ("IN049", "Índice de perdas na distribuição",
     "Percentual do volume de água produzido que se perde até o consumo "
     "(quanto menor, melhor)."),
    ("FN033", "Investimentos totais realizados pelo prestador",
     "Valor em R$ investido pelo prestador de serviços no ano de referência."),
])
pdf.paragrafo(
    "A partir do indicador FN033 e da população total de cada município, "
    "calcula-se o investimento per capita (FN033 / população), permitindo "
    "uma comparação mais justa entre municípios de portes distintos."
)

# ---------------------------------------------------------------------------
# 4. Ferramentas e Tecnologias
# ---------------------------------------------------------------------------
pdf.titulo_secao("Ferramentas e Tecnologias", 4)
pdf.paragrafo(
    "O dashboard foi desenvolvido integralmente em Python, utilizando as "
    "seguintes bibliotecas:"
)
for item in [
    "Streamlit - construção da interface web interativa do dashboard;",
    "Pandas - leitura, tratamento e manipulação dos dados tabulares;",
    "Plotly - criação dos gráficos interativos (barras e rankings).",
]:
    pdf.item_lista(item)
pdf.ln(2)

# ---------------------------------------------------------------------------
# 5. Funcionalidades do Dashboard
# ---------------------------------------------------------------------------
pdf.titulo_secao("Funcionalidades do Dashboard", 5)
for item in [
    "Filtro por município: barra lateral permite selecionar quais "
    "municípios entram nos gráficos comparativos (Sinop é sempre incluído);",
    "Cobertura de água e esgoto: gráficos de barras com IN055 (água) e "
    "IN015 (esgoto), com Sinop destacado e linha de média estadual;",
    "Índice de perdas na distribuição (IN049): gráfico de barras ordenado, "
    "com Sinop destacado;",
    "Investimento per capita: gráfico de barras de FN033/população, com "
    "Sinop destacado;",
    "Ranking de Sinop: tabela mostrando a posição de Sinop entre todos os "
    "municípios de MT para cada indicador, com o respectivo percentil.",
]:
    pdf.item_lista(item)
pdf.ln(2)

# ---------------------------------------------------------------------------
# 6. Resultados e Considerações Finais
# ---------------------------------------------------------------------------
pdf.titulo_secao("Resultados e Considerações Finais", 6)
pdf.paragrafo(
    "O dashboard desenvolvido permite, de forma rápida e visual, identificar "
    "se o município de Sinop está acima ou abaixo da média estadual nos "
    "indicadores de cobertura de água, coleta de esgoto, perdas na "
    "distribuição e investimento per capita, bem como sua posição relativa "
    "(ranking e percentil) frente aos demais 39 municípios de Mato Grosso "
    "com dados completos no SNIS 2022."
)
pdf.paragrafo(
    "Como produto de aprendizagem na disciplina de Ciência de Dados para "
    "Economistas, o projeto exercita competências de coleta e tratamento de "
    "dados públicos, cálculo de indicadores econômicos e sociais, e "
    "comunicação de resultados por meio de visualização de dados, aplicadas "
    "a um problema concreto de política pública - o saneamento básico no "
    "estado de Mato Grosso."
)
pdf.paragrafo(
    "Como trabalhos futuros, sugere-se a inclusão de séries históricas "
    "multianuais (permitindo análise de evolução temporal dos indicadores), "
    "bem como a comparação de Sinop com municípios de outros estados de "
    "porte populacional semelhante."
)

# ---------------------------------------------------------------------------
# 7. Referências
# ---------------------------------------------------------------------------
pdf.titulo_secao("Referências", 7)
pdf.paragrafo(
    "BRASIL. Ministério das Cidades. Sistema Nacional de Informações sobre "
    "Saneamento (SNIS). Informações Desagregadas por Município, Diagnóstico "
    "2022. Disponível em: app4.cidades.gov.br/serieHistorica. "
    "Acesso em: " + data_extenso + "."
)
pdf.paragrafo(
    "IBGE - Instituto Brasileiro de Geografia e Estatística. Estimativas "
    "populacionais dos municípios brasileiros (2021)."
)

pdf.output(OUTPUT_PATH)
print(f"Relatório gerado em: {OUTPUT_PATH}")
