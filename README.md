# Dashboard de Saneamento Básico - Mato Grosso (Benchmarking Sinop)

Dashboard interativo em **Streamlit** para comparar indicadores de
saneamento básico dos municípios de **Mato Grosso**, com foco no
posicionamento de **Sinop (Águas de Sinop)** frente aos demais municípios
do estado.

Indicadores utilizados (fonte: **SNIS - Sistema Nacional de Informações
sobre Saneamento**):

| Código | Indicador | Descrição |
|---|---|---|
| `IN055` | Índice de atendimento total de água | % da população total (urbana + rural) atendida com abastecimento de água |
| `IN015` | Índice de coleta de esgoto | % do volume de água consumido cujo esgoto correspondente é coletado |
| `IN049` | Índice de perdas na distribuição | % do volume de água produzido que se perde até o consumo (quanto menor, melhor) |
| `FN033` | Investimentos totais realizados pelo prestador | Valor em R$ investido pelo prestador no ano de referência |

---

## Sobre os dados incluídos neste repositório

O arquivo `data/snis_mt_2022.csv` contém **dados reais do SNIS** (Diagnóstico
2022, último disponível no momento da atualização):

- **40 dos 142 municípios de MT** — os demais não tinham os indicadores
  `IN055`, `IN015`, `IN049` ou `FN033` informados/preenchidos no SNIS 2022 e
  por isso não entraram no export.
- `codigo_ibge`, `municipio` e `populacao_total` (IBGE 2021) preenchidos a
  partir da lista oficial de municípios de MT.
- `FN033` ausente no SNIS foi tratado como `0` (sem investimento informado).

> Caso surjam Diagnósticos mais recentes, repita o passo a passo abaixo,
> gere `data/snis_mt_AAAA.csv` no mesmo formato e atualize `DATA_PATH` em
> `app.py`.

### Como baixar os dados do SNIS

O portal de série histórica (`app4.mdr.gov.br/serieHistorica` /
`app4.cidades.gov.br/serieHistorica`) é uma aplicação JavaScript que exige
navegação interativa (seleção de UF, município e indicadores na tela) e não
pode ser automatizada por scripts simples. Baixe manualmente:

1. Acesse <https://app4.cidades.gov.br/serieHistorica/> (ou
   <https://app4.mdr.gov.br/serieHistorica/>).
2. Escolha **Informações desagregadas** (ou "Série Histórica por Município").
3. Em **Abrangência**, selecione **Estado: Mato Grosso (MT)** e marque
   **todos os municípios** (ou deixe "Selecionar todos"). Não filtre por
   **Natureza jurídica** — isso exclui municípios com prestadores de
   natureza diferente.
4. Em **Indicadores**, marque `IN055`, `IN015`, `IN049` e `FN033` (eles estão
   em categorias diferentes: IN055/IN049 em "Indicadores - Água", IN015 em
   "Indicadores - Esgotos" e FN033 em "Informações Financeiras").
5. Selecione o **ano mais recente disponível** (no momento da atualização
   deste projeto, o último Diagnóstico completo era referente a 2022).
6. Clique em **Gerar / Exportar** e baixe o arquivo **CSV** (vem em
   UTF-16LE com separador `;` e decimais em vírgula — precisa converter
   antes de usar).

### Formato esperado do CSV (`data/snis_mt_2022.csv`)

O `app.py` espera as seguintes colunas:

```
ano,codigo_ibge,municipio,populacao_total,prestador,IN055,IN015,IN049,FN033
2022,5107909,Sinop,196312,Águas de Sinop S.A.,...,36.9,...,21347506.81
...
```

- `ano`: ano de referência dos dados.
- `codigo_ibge`: código IBGE do município (7 dígitos).
- `municipio`: nome do município **exatamente** como em
  `"Sinop"` (o app procura por esse nome para destacar a concessão).
- `populacao_total`: população total do município (usada para calcular o
  investimento per capita a partir de `FN033`).
- `prestador`: nome do prestador de serviços (informativo, exibido na
  tabela de dados).
- `IN055`, `IN015`, `IN049`, `FN033`: valores dos indicadores baixados do
  SNIS para o ano de referência.

### Regerando o dataset de exemplo

```bash
python scripts/generate_sample_data.py
```

Isso recria `data/snis_mt_2022.csv` com a lista/população reais dos 142
municípios de MT e indicadores sintéticos (Sinop recebe valores fixos
ilustrativos definidos no topo do script) — útil só se o CSV real for
perdido/sobrescrito.

---

## Como executar localmente

```bash
# 1. Criar e ativar um ambiente virtual (opcional, recomendado)
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar o dashboard
streamlit run app.py
```

O dashboard abrirá em `http://localhost:8501`.

---

## Estrutura do projeto

```
.
├── app.py                          # Dashboard principal (Streamlit)
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
├── data/
│   └── snis_mt_2022.csv            # Dados reais do SNIS (40 municipios, ano 2022)
└── scripts/
    └── generate_sample_data.py     # Gera o dataset de exemplo/placeholder
```

---

## Deploy no Streamlit Community Cloud

1. Crie um repositório no GitHub e suba estes arquivos (incluindo
   `data/snis_mt_2022.csv` com os dados reais do SNIS):

   ```bash
   git init
   git add .
   git commit -m "Dashboard de saneamento MT - benchmarking Sinop"
   git branch -M main
   git remote add origin https://github.com/<seu-usuario>/<seu-repo>.git
   git push -u origin main
   ```

2. Acesse <https://share.streamlit.io/>, faça login com sua conta GitHub.
3. Clique em **New app**, selecione o repositório, branch `main` e o
   arquivo principal `app.py`.
4. Clique em **Deploy**. O Streamlit Cloud instalará automaticamente as
   dependências listadas em `requirements.txt`.

---

## Funcionalidades do dashboard

- **Filtro por município**: barra lateral permite selecionar quais
  municípios entram nos gráficos comparativos (Sinop é sempre incluído).
- **Cobertura de água e esgoto**: gráficos de barras com IN055 (água) e
  IN015 (esgoto), Sinop destacado em vermelho, com linha de média estadual.
- **Índice de perdas na distribuição (IN049)**: gráfico de barras ordenado,
  Sinop destacado.
- **Investimento per capita**: `FN033 / população`, gráfico de barras com
  Sinop destacado.
- **Ranking de Sinop**: tabela mostrando a posição de Sinop entre todos os
  municípios de MT para cada indicador, com percentil.
