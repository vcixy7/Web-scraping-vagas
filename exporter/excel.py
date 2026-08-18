# exportação das vagas para uma planilha Excel usando pandas
import pandas as pd

# de qual campo interno vem cada coluna do Excel (nesta ordem)
COLUNAS = {
    "titulo": "Título",
    "empresa": "Empresa",
    "local": "Local",
    "estado": "Estado (UF)",
    "salario_texto": "Salário",
    "url": "Link",
}


def salvar_excel(vagas, nome_arquivo="vagas.xlsx"):
    linhas = [{coluna: vaga.get(campo) for campo, coluna in COLUNAS.items()} for vaga in vagas]
    df = pd.DataFrame(linhas, columns=list(COLUNAS.values()))
    df.to_excel(nome_arquivo, index=False)
