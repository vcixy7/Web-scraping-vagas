# entrada não-interativa: lê o cargo da variável de ambiente COLETA_CARGO e coleta.
# Serve para rodar de forma automatizada (agendador local, CI, etc.).
import os
import sys

# garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.coletor import coletar
from exporter.excel import salvar_excel
from database.db import iniciar_banco, registrar_pesquisa, salvar_vagas


def main():
    cargo = os.getenv("COLETA_CARGO", "desenvolvedor").strip()

    iniciar_banco()
    pesquisa_id = registrar_pesquisa(cargo)

    print(f"Coletando vagas para: {cargo}")
    vagas = coletar(cargo)

    if not vagas:
        print("Nenhuma vaga encontrada.")
        return

    novas, duplicadas = salvar_vagas(vagas, pesquisa_id=pesquisa_id)
    salvar_excel(vagas)
    print(f"{len(vagas)} vagas coletadas — {novas} novas, {duplicadas} já existiam.")


if __name__ == "__main__":
    main()
