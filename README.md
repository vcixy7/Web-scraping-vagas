📊 Web Scraping de Vagas de Emprego

Este projeto realiza web scraping de vagas de emprego a partir de sites de busca de vagas, coletando informações relevantes e exportando os dados para uma planilha Excel, facilitando análises e consultas.

O objetivo do projeto é automatizar a coleta de vagas, simulando um cenário real de uso de automação em empresas de RH, recrutamento ou análise de mercado de trabalho.

🚀 Funcionalidades

🔍 Busca de vagas a partir de um cargo informado pelo usuário

🌎 Extração de informações como:

Título da vaga

Empresa

Estado (UF)

Salário (quando disponível)

📄 Exportação automática dos dados para arquivo Excel (.xlsx)

🧩 Estrutura de projeto modular e organizada

🛠️ Tecnologias Utilizadas

Python 3

Selenium – automação do navegador

Pandas – manipulação de dados

OpenPyXL – geração de planilhas Excel

WebDriver Manager – gerenciamento do driver do navegador

Git & GitHub – versionamento e portfólio

📁 Estrutura do Projeto
web-scraping-vagas-de-emprego/

│
├── main/

│   └── main.py               # Arquivo principal do projeto
│

├── scraper/

│   ├── browser.py            # Configuração do navegador (Selenium)

│   └── parser.py             # Extração e tratamento das vagas
│

├── exporter/

│   └── excel.py              # Exportação dos dados para Excel

├── requirements.txt          # Dependências do projeto

└── README.md                 # Documentação

▶️ Como Executar o Projeto

1️⃣ Clonar o repositório
git clone https://github.com/vcixy7/Web-scraping-vagas.git

cd Web-scraping-de-vagas-

2️⃣ Instalar as dependências

pip install -r requirements.txt

3️⃣ Executar o projeto

python main/main.py
**ou**
py main/main.py

4️⃣ Informar o cargo desejado

O programa solicitará o cargo e iniciará a busca automaticamente.

📊 Resultado

Ao final da execução, será gerado um arquivo Excel (.xlsx) contendo as vagas encontradas, incluindo cargo, empresa, estado e salário (quando disponível).

🎯 Objetivo do Projeto

Este projeto foi desenvolvido com foco em:

Aprendizado prático de web scraping

Organização de código em projetos Python

Automação aplicada a problemas reais

Construção de portfólio profissional

📌 Observações

Alguns sites podem aplicar bloqueios ou limitações ao scraping.

O projeto utiliza Selenium para simular o comportamento de um usuário real.

👤 Autor

Vinícius Araújo

Estudante de tecnologia | Python | Automação | Web Scraping
