import os
import sys

# garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.coletor import coletar
from exporter.excel import salvar_excel
from database.db import iniciar_banco, registrar_pesquisa, salvar_vagas, contar_vagas


def main():
    cargo = input("Digite o cargo desejado: ").strip()
    if not cargo:
        print("Nenhum cargo informado.")
        return

    iniciar_banco()
    registrar_pesquisa(cargo)

    print("\nBuscando vagas...")
    vagas = coletar(cargo)

    if not vagas:
        print("Nenhuma vaga encontrada.")
        return

    novas, duplicadas = salvar_vagas(vagas)
    salvar_excel(vagas)

    print(f"\n{len(vagas)} vagas coletadas.")
    print(f"{novas} novas salvas no banco ({duplicadas} já estavam lá). Total acumulado: {contar_vagas()}.")
    print("Planilha atualizada: vagas.xlsx")


if __name__ == "__main__":
    main()
