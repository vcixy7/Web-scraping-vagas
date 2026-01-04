# importer pandas para manipulação de Excel
import pandas as pd

def salvar_excel(vagas, nome_arquivo="vagas.xlsx"):
    df = pd.DataFrame(vagas)
    df.to_excel(nome_arquivo, index=False)
