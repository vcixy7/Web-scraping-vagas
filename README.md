# Web Scraping de Vagas

Aplicação em Python para **coleta, processamento e análise de vagas de emprego** provenientes de múltiplas fontes.

O sistema integra scraping com Selenium e APIs de vagas, normaliza os dados coletados, identifica tecnologias mencionadas nas oportunidades, evita duplicações e persiste os resultados em SQLite.

Também disponibiliza exportação para Excel, relatórios pelo terminal e um dashboard desenvolvido com Streamlit.

## Funcionalidades

* Coleta de vagas em múltiplas fontes.
* Integração com **Indeed, Remotive, RemoteOK e Adzuna**.
* Extração de:

  * cargo;
  * empresa;
  * localização;
  * estado (UF);
  * modalidade de trabalho;
  * salário;
  * tecnologias mencionadas;
  * URL da vaga;
  * fonte.
* Normalização automática dos dados coletados.
* Conversão de salários para valor médio mensal.
* Identificação de tecnologias por palavras-chave.
* Persistência das vagas em **SQLite**.
* Prevenção de registros duplicados pela URL.
* Histórico das pesquisas realizadas.
* Exportação dos resultados para **Excel**.
* Relatórios pelo terminal.
* Dashboard web com **Streamlit**.
* Arquitetura modular para inclusão de novas fontes.

## Fontes de dados

### Indeed

Coleta realizada com **Selenium**, utilizando Chrome para acessar e processar os resultados.

### Remotive

Integração através da API pública da plataforma, com foco em oportunidades remotas de tecnologia.

### RemoteOK

Integração através da API pública de vagas remotas.

### Adzuna

Integração opcional através da API oficial.

Para utilizar essa fonte, configure as credenciais:

```bash
# Windows PowerShell
$env:ADZUNA_APP_ID="seu_id"
$env:ADZUNA_APP_KEY="sua_chave"
```

Linux/macOS:

```bash
export ADZUNA_APP_ID="seu_id"
export ADZUNA_APP_KEY="sua_chave"
```

## Arquitetura

Cada fonte de vagas funciona como um módulo independente dentro de `fontes/`.

Todos os módulos seguem uma interface semelhante:

```python
coletar(cargo, limite)
```

Isso permite adicionar novas fontes sem alterar o fluxo principal da aplicação.

```text
main/
  main.py

fontes/
  indeed.py
  remotive.py
  remoteok.py
  adzuna.py
  comum.py

scraper/
  browser.py
  parser.py
  coletor.py
  tecnologias.py
  util.py

database/
  db.py
  consultas.py

exporter/
  excel.py

scripts/
  coleta_agendada.py

.github/workflows/
  coleta.yml

streamlit_app.py
relatorio.py
```

### Responsabilidades

* `fontes/` — integrações com as plataformas de vagas.
* `scraper/` — scraping, parsing e processamento dos dados.
* `database/` — persistência e consultas SQLite.
* `exporter/` — exportação dos resultados.
* `streamlit_app.py` — dashboard e interface web.
* `relatorio.py` — geração de relatórios pelo terminal.

## Tecnologias

* Python
* Selenium
* Requests
* Pandas
* OpenPyXL
* SQLite
* Streamlit
* WebDriver Manager
* GitHub Actions

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/vcixy7/WebScraping.git
cd WebScraping
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a coleta

```bash
python main/main.py
```

Durante a execução, é possível informar o cargo pesquisado e selecionar as fontes utilizadas.

Os resultados são armazenados no SQLite e também podem ser exportados para `vagas.xlsx`.

## Relatório

Para visualizar um resumo das vagas armazenadas:

```bash
python relatorio.py
```

## Dashboard

Para iniciar a interface web:

```bash
streamlit run streamlit_app.py
```

O dashboard permite visualizar os dados coletados, gráficos, distribuição das vagas por fonte e histórico de pesquisas.

## Coleta automatizada

O projeto também possui um modo de execução sem interação pelo terminal:

```bash
COLETA_CARGO="desenvolvedor python" COLETA_FONTES="remotive,remoteok" python scripts/coleta_agendada.py
```

As configurações são recebidas através de variáveis de ambiente.

Um workflow em `.github/workflows/coleta.yml` permite executar esse processo através do **GitHub Actions**.

## Limitações

A coleta do Indeed depende da estrutura HTML da plataforma e pode exigir ajustes caso a página seja alterada.

A identificação de tecnologias utiliza correspondência por palavras-chave e, portanto, representa uma aproximação baseada no conteúdo disponível nas vagas.

## Autor

**Vinícius Araújo**
Análise e Desenvolvimento de Sistemas

GitHub: [@vcixy7](https://github.com/vcixy7)
