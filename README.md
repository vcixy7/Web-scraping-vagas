# Web scraping de vagas

Projeto pessoal que fiz para praticar automação e coleta de dados com Python. Ele pesquisa um cargo em **vários sites de uma vez**, junta as vagas em um banco (sem repetir), identifica as tecnologias pedidas e ainda tem relatório e uma interface web.

Comecei só com o Indeed via Selenium e fui separando o código em módulos conforme foi crescendo. Hoje cada site é uma "fonte" plugável, os dados ficam em SQLite e dá para acompanhar tudo por um painel. É um projeto de estudo, então continua evoluindo.

## O que já funciona

- **Pesquisa em várias fontes ao mesmo tempo**: Indeed (Selenium), Remotive e RemoteOK (APIs públicas) e Adzuna (API oficial, opcional).
- **Extração** de cada vaga: título, empresa, local, estado (UF), modalidade (remoto/híbrido/presencial), salário, tecnologias citadas, link e a fonte.
- **Normalização**: tira a UF do local, padroniza a modalidade e transforma o salário em valor médio mensal em reais.
- **Banco SQLite** (`data/vagas.db`) que **não repete** vagas (pela URL) e guarda um **histórico das pesquisas**.
- **Relatório no terminal** (`python relatorio.py`) e **interface web** (Streamlit) com painel, gráficos (inclusive vagas por fonte) e o histórico.
- **Exportação para Excel** (`vagas.xlsx`).

## Fontes de vagas

Cada fonte é um módulo dentro de `fontes/`, com uma função `coletar(cargo, limite)` que devolve as vagas no mesmo formato. Para adicionar um site novo, basta criar mais um módulo assim. Hoje existem:

- **Indeed** — via Selenium (abre o Chrome). Cobertura ampla, mas depende do HTML e pode quebrar quando o site muda.
- **Remotive** e **RemoteOK** — APIs públicas de vagas remotas de tecnologia. Não precisam de chave e são bem estáveis.
- **Adzuna** — API oficial, cobertura ampla (inclui Brasil). Só entra em ação se você configurar as chaves grátis:

```bash
# Windows (PowerShell)
$env:ADZUNA_APP_ID="seu_id"; $env:ADZUNA_APP_KEY="sua_chave"
# Linux / macOS
export ADZUNA_APP_ID=seu_id ADZUNA_APP_KEY=sua_chave
```
(as chaves saem de graça em https://developer.adzuna.com/)

### E o LinkedIn?

Não incluí o LinkedIn de propósito. Ele exige login para ver as vagas de verdade, bloqueia automação de forma agressiva e o scraping vai contra os termos de uso — não compensa o risco nem seria estável. Preferi APIs públicas e a do Adzuna, que são permitidas e não quebram como HTML. Se um dia fizer sentido, é só criar um módulo novo em `fontes/`.

## Como rodar

Você precisa ter o Python 3 instalado (e o Google Chrome, se for usar o Indeed). O driver do Chrome é baixado automaticamente pelo `webdriver-manager`.

```bash
# 1. clonar o repositório
git clone https://github.com/vcixy7/Web-scraping-vagas.git
cd Web-scraping-vagas

# 2. (opcional) criar um ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# 3. instalar as dependências
pip install -r requirements.txt

# 4. executar
python main/main.py
```

O programa pergunta o cargo e quais fontes usar (enter = todas), coleta, guarda no banco e salva o `vagas.xlsx`. Como as fontes de API não abrem navegador, dá para pesquisar rápido sem depender do Chrome.

Depois, para ver um resumo:

```bash
python relatorio.py
```

Ou a interface, com a busca e o painel:

```bash
streamlit run streamlit_app.py
```

## Automação (modelo)

Existe um script que roda a coleta sem digitar nada, lendo o cargo e as fontes de variáveis de ambiente:

```bash
COLETA_CARGO="desenvolvedor python" COLETA_FONTES="remotive,remoteok" python scripts/coleta_agendada.py
```

E há um workflow de exemplo em `.github/workflows/coleta.yml` para rodar no GitHub Actions. Ele está configurado para rodar **só manualmente** — coletar de sites de terceiros de forma agendada pode esbarrar nos termos de uso, então deixei o agendamento comentado de propósito.

## Como o projeto está organizado

```
main/
  main.py            # ponto de entrada no terminal
fontes/
  indeed.py          # fonte Indeed (Selenium)
  remotive.py        # fonte Remotive (API)
  remoteok.py        # fonte RemoteOK (API)
  adzuna.py          # fonte Adzuna (API oficial, opcional)
  comum.py           # monta a vaga no formato padrão (normaliza + tecnologias)
scraper/
  browser.py         # sobe o Chrome com o Selenium (headless via HEADLESS=1)
  parser.py          # extrai os dados de cada card do Indeed
  coletor.py         # junta browser + parser para o Indeed
  tecnologias.py     # identifica tecnologias citadas no texto
  util.py            # apoio: UF, modalidade, salário e formatação em R$
database/
  db.py              # cria o banco SQLite e salva as vagas (sem duplicar)
  consultas.py       # consultas de leitura para o relatório e a interface
exporter/
  excel.py           # salva a lista de vagas no Excel
scripts/
  coleta_agendada.py # coleta sem interação (lê cargo/fontes do ambiente)
.github/workflows/
  coleta.yml         # modelo de automação (rodar manual; ver os avisos)
streamlit_app.py     # interface web: pesquisa + painel + histórico
relatorio.py         # resumo das vagas no terminal
data/
  vagas.db           # banco criado na primeira execução (não versionado)
```

## Tecnologias

Python 3, Selenium, Requests (APIs), Pandas, OpenPyXL (Excel), WebDriver Manager, SQLite e Streamlit.

## Próximos passos

- Filtros na interface (por estado, modalidade, tecnologia).
- Ler a descrição completa das vagas do Indeed (as fontes de API já trazem a descrição, então a extração de tecnologias delas é melhor).
- Mais fontes de vagas — a arquitetura já facilita adicionar.
- Colocar a interface no ar (deploy).

## Observações

A fonte do Indeed depende do HTML da página; se ele mudar, é preciso ajustar o `parser.py` (por isso ele tenta vários seletores). A identificação de tecnologias é por palavra-chave, então é uma aproximação. Sites têm termos de uso — a intenção aqui é estudo e uso pessoal, e por isso dei preferência a APIs públicas/oficiais.

## Autor

Vinícius Araújo — estudante de Análise e Desenvolvimento de Sistemas.
GitHub: [@vcixy7](https://github.com/vcixy7)
