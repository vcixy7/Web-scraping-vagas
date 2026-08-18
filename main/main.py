import os
import sys

# garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fontes import coletar_de, nomes
from exporter.excel import salvar_excel
from database.db import iniciar_banco, registrar_pesquisa, salvar_vagas, contar_vagas


def main():
    cargo = input("Digite o cargo desejado: ").strip()
    if not cargo:
        print("Nenhum cargo informado.")
        return

    print("Fontes disponíveis:", ", ".join(nomes()))
    escolha = input("Quais fontes usar? (separe por vírgula, enter = todas): ").strip()
    fontes_escolhidas = [n.strip() for n in escolha.split(",") if n.strip()] or nomes()

    iniciar_banco()
    pesquisa_id = registrar_pesquisa(cargo)

    print("\nBuscando vagas...")
    vagas = coletar_de(cargo, fontes_escolhidas)

    if not vagas:
        print("Nenhuma vaga encontrada.")
        return

    novas, duplicadas = salvar_vagas(vagas, pesquisa_id=pesquisa_id)
    salvar_excel(vagas)

    print(f"\n{len(vagas)} vagas coletadas de {len(fontes_escolhidas)} fonte(s).")
    print(f"{novas} novas salvas no banco ({duplicadas} já estavam lá). Total acumulado: {contar_vagas()}.")
    print("Planilha atualizada: vagas.xlsx")


if __name__ == "__main__":
    main()
