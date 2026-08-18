# Web scraping de vagas

Projeto pessoal que fiz para praticar automação e coleta de dados com Python. Ele abre o Indeed, pesquisa por um cargo que você informa e guarda as vagas encontradas — em um banco SQLite e também em uma planilha do Excel.

Comecei com um script único que só exportava para o Excel e fui separando o código em módulos conforme foi crescendo. Hoje ele já guarda as vagas em banco (sem duplicar), tem um relatório no terminal e uma interface web simples. Ainda está em evolução, mas essa base já funciona bem.

## O que já funciona

- Busca por cargo, informado pelo usuário no terminal.
- Para cada vaga, coleta título, empresa, local, estado (UF), salário e link.
- Um tratamento básico dos dados: extrai a UF a partir do texto do local e normaliza o salário — junta faixas pela média, converte valores por ano/hora/dia para o mês e formata em reais.
- Salva tudo em um banco SQLite (`data/vagas.db`) e não repete vagas que já foram guardadas (usa o link como referência).
- Também exporta o resultado para um arquivo `vagas.xlsx`.
- Tem um relatório no terminal (`python relatorio.py`) com totais, empresas com mais vagas, distribuição por estado e salário médio.
- Tem também uma interface web simples (Streamlit) para pesquisar e ver os resultados e um painel com os números.

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

Se preferir uma tela em vez do terminal, tem também uma interface simples:

```bash
pip install streamlit
streamlit run streamlit_app.py
```

Ela abre no navegador uma página onde você digita o cargo, clica em **Pesquisar** e vê as vagas coletadas, mais um resumo com os totais e alguns gráficos.

## Como o projeto está organizado

```
main/
  main.py       # ponto de entrada: pede o cargo, monta a busca e junta tudo
scraper/
  browser.py       # sobe o Chrome com o Selenium
  parser.py        # varre os cards da página e extrai os dados de cada vaga
  coletor.py       # junta browser + parser: faz a busca e devolve as vagas
  util.py          # funções de apoio: UF, salário e formatação em R$
database/
  db.py            # cria o banco SQLite e salva as vagas (sem duplicar)
  consultas.py     # consultas de leitura usadas pelo relatório e pela interface
exporter/
  excel.py         # salva a lista de vagas no Excel
streamlit_app.py   # interface web: pesquisa + painel com os números
relatorio.py       # resumo das vagas guardadas no banco (no terminal)
data/
  vagas.db         # banco criado na primeira execução (não versionado)
```

## Tecnologias

Python 3, Selenium (automação do navegador), Pandas, OpenPyXL (geração do Excel) e WebDriver Manager (para o driver do Chrome).

## Próximos passos

Coisas que pretendo fazer conforme for aprendendo:

- Uma tela para consultar e filtrar o histórico das pesquisas já feitas (a tabela `pesquisas` já vai sendo gravada a cada busca).
- Identificar as tecnologias citadas nas descrições (Java, Python, SQL...) para ver o que aparece com mais frequência.
- Melhorar as análises e os gráficos (por enquanto o painel mostra o básico).

## Observações

A coleta depende do HTML do Indeed. Se a página mudar, os seletores podem parar de funcionar e é preciso ajustar o `parser.py` — por isso o `parser` tenta vários seletores antes de desistir. Uso o Selenium justamente para dar conta do carregamento dinâmico. Vale lembrar também que sites têm termos de uso; aqui a intenção é estudo e uso pessoal.

## Autor

Vinícius Araújo — estudante de Análise e Desenvolvimento de Sistemas.
GitHub: [@vcixy7](https://github.com/vcixy7)
