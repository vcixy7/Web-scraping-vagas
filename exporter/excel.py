# exportação das vagas para uma planilha Excel usando pandas
import pandas as pd

COLUNAS = ["Título", "Empresa", "Local", "Estado (UF)", "Modalidade", "Salário", "Tecnologias", "Fonte", "Link"]


def salvar_excel(vagas, nome_arquivo="vagas.xlsx"):
    linhas = []
    for vaga in vagas:
        linhas.append({
            "Título": vaga.get("titulo"),
            "Empresa": vaga.get("empresa"),
            "Local": vaga.get("local"),
            "Estado (UF)": vaga.get("estado"),
            "Modalidade": vaga.get("modalidade"),
            "Salário": vaga.get("salario_texto"),
            "Tecnologias": ", ".join(vaga.get("tecnologias", [])),
            "Fonte": vaga.get("fonte"),
            "Link": vaga.get("url"),
        })
    df = pd.DataFrame(linhas, columns=COLUNAS)
    df.to_excel(nome_arquivo, index=False)
