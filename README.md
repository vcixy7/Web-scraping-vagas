# Web scraping de vagas

Projeto pessoal que fiz para praticar automação e coleta de dados com Python. Ele abre o Indeed, pesquisa por um cargo que você digita no terminal e junta as vagas encontradas em uma planilha do Excel.

Comecei com um script único e fui separando o código em módulos conforme foi crescendo. Ainda está em evolução — a ideia é chegar em um fluxo mais completo, com banco de dados, uma interface e algumas análises —, mas por enquanto o que já funciona bem é a parte de coletar e exportar.

## O que já funciona

- Busca por cargo, informado pelo usuário no terminal.
- Para cada vaga, coleta título, empresa, local, estado (UF), salário e link.
- Um tratamento básico dos dados: extrai a UF a partir do texto do local e normaliza o salário — junta faixas pela média, converte valores por ano/hora/dia para o mês e formata em reais.
- Salva tudo em um banco SQLite (`data/vagas.db`) e não repete vagas que já foram guardadas (usa o link como referência).
- Também exporta o resultado para um arquivo `vagas.xlsx`.

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

O programa pede o cargo, abre o navegador, faz a coleta e salva o `vagas.xlsx` na pasta onde você rodou o comando.

## Como o projeto está organizado

```
main/
  main.py       # ponto de entrada: pede o cargo, monta a busca e junta tudo
scraper/
  browser.py    # sobe o Chrome com o Selenium
  parser.py     # varre os cards da página e extrai os dados de cada vaga
  util.py       # funções de apoio: UF, salário e formatação em R$
database/
  db.py         # cria o banco SQLite e salva as vagas (sem duplicar)
exporter/
  excel.py      # salva a lista de vagas no Excel
data/
  vagas.db      # banco criado na primeira execução (não versionado)
```

## Tecnologias

Python 3, Selenium (automação do navegador), Pandas, OpenPyXL (geração do Excel) e WebDriver Manager (para o driver do Chrome).

## Próximos passos

Coisas que pretendo fazer conforme for aprendendo:

- Uma interface simples para pesquisar sem precisar do terminal (provavelmente com Streamlit).
- Um histórico das pesquisas já feitas (a tabela `pesquisas` já vai sendo gravada a cada busca).
- Identificar as tecnologias citadas nas descrições (Java, Python, SQL...) para ver o que aparece com mais frequência.
- Alguns gráficos e análises em cima dos dados coletados.

## Observações

A coleta depende do HTML do Indeed. Se a página mudar, os seletores podem parar de funcionar e é preciso ajustar o `parser.py` — por isso o `parser` tenta vários seletores antes de desistir. Uso o Selenium justamente para dar conta do carregamento dinâmico. Vale lembrar também que sites têm termos de uso; aqui a intenção é estudo e uso pessoal.

## Autor

Vinícius Araújo — estudante de Análise e Desenvolvimento de Sistemas.
GitHub: [@vcixy7](https://github.com/vcixy7)
