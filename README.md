# Dashboard de Saneamento Básico - Mato Grosso (Benchmarking Sinop)

Dashboard interativo em **Streamlit** para comparar indicadores de
saneamento básico dos municípios de **Mato Grosso**, com foco no
posicionamento de **Sinop (Águas de Sinop)** frente aos demais municípios
do estado.

Indicadores utilizados (fonte: **SNIS - Sistema Nacional de Informações
sobre Saneamento**):

| Código | Indicador | Descrição |
|---|---|---|
| `IN023` | Índice de atendimento urbano de água | % da população urbana atendida com abastecimento de água |
| `IN015` | Índice de coleta de esgoto | % do volume de água consumido cujo esgoto correspondente é coletado |
| `IN049` | Índice de perdas na distribuição | % do volume de água produzido que se perde até o consumo (quanto menor, melhor) |
| `FN033` | Investimentos totais realizados pelo prestador | Valor em R$ investido pelo prestador no ano de referência |

---

## ⚠️ Sobre os dados incluídos neste repositório

O arquivo `data/snis_mt_2023.csv` contém:

- **Lista real** dos 142 municípios de Mato Grosso e sua **população real**
  (estimativas IBGE 2021), obtidos via API pública do IBGE.
- **Valores de IN023, IN015, IN049 e FN033 SINTÉTICOS** (gerados por
  `scripts/generate_sample_data.py`), usados apenas como placeholder para
  que o dashboard funcione "out of the box" durante o desenvolvimento.

> Antes de usar este projeto para análises reais/acadêmicas, **substitua
> `data/snis_mt_2023.csv` pelos dados oficiais do SNIS**, seguindo o passo a
> passo abaixo. O código não foi alterado de forma alguma - basta trocar o
> arquivo CSV mantendo as colunas no mesmo formato.

### Como baixar os dados reais do SNIS

O portal oficial (`app4.mdr.gov.br/serieHistorica`) é uma aplicação
JavaScript que exige navegação interativa (seleção de UF, município e
indicadores na tela) e não pode ser automatizada por scripts simples. Baixe
manualmente:

1. Acesse <https://app4.mdr.gov.br/serieHistorica/>.
2. Em **Tipo de pesquisa**, selecione **Série Histórica por Município**.
3. Em **Abrangência**, selecione **Estado: Mato Grosso (MT)** e marque
   **todos os municípios** (ou deixe "Selecionar todos").
4. Em **Indicadores**, marque `IN023`, `IN015`, `IN049` e `FN033` (eles estão
   em categorias diferentes: IN023/IN049 em "Indicadores - Água", IN015 em
   "Indicadores - Esgotos" e FN033 em "Informações Financeiras").
5. Selecione o **ano mais recente disponível** (no momento da criação deste
   projeto, o último Diagnóstico publicado era referente a 2023).
6. Clique em **Gerar / Exportar** e baixe o arquivo **CSV**.

### Formato esperado do CSV (`data/snis_mt_2023.csv`)

O `app.py` espera as seguintes colunas (renomeie/ajuste o CSV exportado do
SNIS para este formato):

```
ano,codigo_ibge,municipio,populacao_total,prestador,IN023,IN015,IN049,FN033
2023,5107909,Sinop,148960,Águas de Sinop,99.4,78.2,31.5,18500000.0
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
- `IN023`, `IN015`, `IN049`, `FN033`: valores dos indicadores baixados do
  SNIS para o ano de referência.

### Regerando o dataset de exemplo

```bash
python scripts/generate_sample_data.py
```

Isso recria `data/snis_mt_2023.csv` com a lista/população reais dos 142
municípios de MT e indicadores sintéticos (Sinop recebe valores fixos
ilustrativos definidos no topo do script).

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
│   └── snis_mt_2023.csv            # Dados (substituir pelos dados reais do SNIS)
└── scripts/
    └── generate_sample_data.py     # Gera o dataset de exemplo/placeholder
```

---

## Deploy no Streamlit Community Cloud

1. Crie um repositório no GitHub e suba estes arquivos (incluindo
   `data/snis_mt_2023.csv` com os dados reais do SNIS):

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
- **Cobertura de água e esgoto**: gráficos de barras com IN023 (água) e
  IN015 (esgoto), Sinop destacado em vermelho, com linha de média estadual.
- **Índice de perdas na distribuição (IN049)**: gráfico de barras ordenado,
  Sinop destacado.
- **Investimento per capita**: `FN033 / população`, gráfico de barras com
  Sinop destacado.
- **Ranking de Sinop**: tabela mostrando a posição de Sinop entre todos os
  municípios de MT para cada indicador, com percentil.
