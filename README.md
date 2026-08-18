# Web scraping de vagas

Projeto pessoal que fiz para praticar automação e coleta de dados com Python. Ele abre o Indeed, pesquisa por um cargo que você informa e guarda as vagas encontradas — em um banco SQLite e também em uma planilha do Excel — com um relatório e uma interface web por cima.

Comecei com um script único que só exportava para o Excel e fui separando o código em módulos conforme foi crescendo. Hoje ele já guarda as vagas em banco (sem duplicar), identifica tecnologias, tem um relatório no terminal e uma interface simples em Streamlit. É um projeto de estudo, então continua evoluindo.

## O que já funciona

- **Pesquisa por cargo**, pelo terminal ou pela interface web.
- **Extração** de cada vaga: título, empresa, local, estado (UF), modalidade (remoto/híbrido/presencial), salário, link e as **tecnologias** citadas no texto (Python, SQL, Docker...).
- **Normalização**: tira a UF do texto do local, padroniza a modalidade e transforma o salário em um valor médio mensal em reais (juntando faixas e convertendo por ano/hora/dia).
- **Banco SQLite** (`data/vagas.db`) que **não repete** vagas já guardadas (usa o link como referência) e mantém um **histórico das pesquisas** feitas.
- **Relatório no terminal** (`python relatorio.py`): totais, empresas com mais vagas, distribuição por estado e modalidade, tecnologias mais pedidas, evolução por dia e o histórico.
- **Interface web** (Streamlit): pesquisar, ver os resultados em tabela, um painel com gráficos e o histórico das buscas.
- **Exportação para Excel** (`vagas.xlsx`).

## Como rodar

Você precisa ter o Python 3 e o Google Chrome instalados. O driver do Chrome é baixado automaticamente pelo `webdriver-manager`, então não precisa configurar nada à mão.

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

O programa pede o cargo, abre o navegador, faz a coleta, guarda as vagas no banco e salva o `vagas.xlsx` na pasta onde você rodou o comando.

Depois de coletar, dá para ver um resumo do que está no banco:

```bash
python relatorio.py
```

Se preferir uma tela em vez do terminal, tem também a interface:

```bash
streamlit run streamlit_app.py
```

Ela abre no navegador uma página onde você digita o cargo, clica em **Pesquisar** e vê as vagas coletadas, mais um painel com os totais, gráficos e o histórico das pesquisas.

## Automação (modelo)

Existe um script que roda a coleta sem precisar digitar nada — ele lê o cargo da variável de ambiente `COLETA_CARGO`:

```bash
COLETA_CARGO="desenvolvedor python" HEADLESS=1 python scripts/coleta_agendada.py
```

E há um workflow de exemplo em `.github/workflows/coleta.yml` para rodar isso no GitHub Actions. Ele está configurado para rodar **só manualmente**: coletar de sites de terceiros de forma agendada pode esbarrar nos termos de uso, então deixei o agendamento comentado de propósito.

## Como o projeto está organizado

```
main/
  main.py            # ponto de entrada no terminal
scraper/
  browser.py         # sobe o Chrome com o Selenium (headless opcional via HEADLESS=1)
  parser.py          # extrai os dados de cada card de vaga
  coletor.py         # junta browser + parser: faz a busca e devolve as vagas
  tecnologias.py     # identifica tecnologias citadas no texto da vaga
  util.py            # apoio: UF, modalidade, salário e formatação em R$
database/
  db.py              # cria o banco SQLite e salva as vagas (sem duplicar)
  consultas.py       # consultas de leitura para o relatório e a interface
exporter/
  excel.py           # salva a lista de vagas no Excel
scripts/
  coleta_agendada.py # coleta sem interação (lê o cargo de COLETA_CARGO)
.github/workflows/
  coleta.yml         # modelo de automação (rodar manual; ver os avisos)
streamlit_app.py     # interface web: pesquisa + painel + histórico
relatorio.py         # resumo das vagas no terminal
data/
  vagas.db           # banco criado na primeira execução (não versionado)
```

## Tecnologias

Python 3, Selenium (automação do navegador), Pandas, OpenPyXL (Excel), WebDriver Manager (driver do Chrome), SQLite (banco) e Streamlit (interface).

## Próximos passos

Coisas que pretendo fazer conforme for aprendendo:

- Ler a **descrição completa** de cada vaga — hoje as tecnologias vêm só do texto do card, então dá para melhorar bastante.
- Filtros na interface (por estado, modalidade, tecnologia).
- Suporte a outras fontes de vagas além do Indeed.
- Colocar a interface no ar (deploy) para não depender de rodar local.

## Observações

A coleta depende do HTML do Indeed. Se a página mudar, os seletores podem parar de funcionar e é preciso ajustar o `parser.py` — por isso ele tenta vários seletores antes de desistir. A identificação de tecnologias é por palavra-chave, então é uma aproximação. Uso o Selenium justamente para dar conta do carregamento dinâmico. Vale lembrar também que sites têm termos de uso; aqui a intenção é estudo e uso pessoal.

## Autor

Vinícius Araújo — estudante de Análise e Desenvolvimento de Sistemas.
GitHub: [@vcixy7](https://github.com/vcixy7)
