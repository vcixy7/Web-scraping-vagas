# entrada não-interativa: lê o cargo e as fontes de variáveis de ambiente e coleta.
# Serve para rodar de forma automatizada (agendador local, CI, etc.).
#   COLETA_CARGO  -> cargo a pesquisar (padrão "desenvolvedor")
#   COLETA_FONTES -> fontes separadas por vírgula (padrão "remotive,remoteok")
import os
import sys

# garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fontes import coletar_de, nomes
from exporter.excel import salvar_excel
from database.db import iniciar_banco, registrar_pesquisa, salvar_vagas


def main():
    cargo = os.getenv("COLETA_CARGO", "desenvolvedor").strip()
    fontes_env = os.getenv("COLETA_FONTES", "remotive,remoteok")
    fontes_escolhidas = [n.strip() for n in fontes_env.split(",") if n.strip()] or nomes()

    iniciar_banco()
    pesquisa_id = registrar_pesquisa(cargo)

    print(f"Coletando '{cargo}' em: {', '.join(fontes_escolhidas)}")
    vagas = coletar_de(cargo, fontes_escolhidas)

    if not vagas:
        print("Nenhuma vaga encontrada.")
        return

    novas, duplicadas = salvar_vagas(vagas, pesquisa_id=pesquisa_id)
    salvar_excel(vagas)
    print(f"{len(vagas)} vagas coletadas — {novas} novas, {duplicadas} já existiam.")


if __name__ == "__main__":
    main()
