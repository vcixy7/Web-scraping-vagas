import os
import sys

# garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db import iniciar_banco
from database import consultas
from scraper.util import format_brl


def main():
    iniciar_banco()  # garante que as tabelas existam, mesmo sem ter coletado ainda

    if consultas.total_vagas() == 0:
        print("Ainda não há vagas no banco. Rode primeiro: python main/main.py")
        return

    print("=== Resumo das vagas coletadas ===\n")

    print(f"Vagas no banco:   {consultas.total_vagas()}")
    print(f"Empresas:         {consultas.total_empresas()}")

    media = consultas.salario_medio()
    print(f"Salário médio:    {format_brl(media) if media else 'sem dados suficientes'}")

    print("\nEmpresas com mais vagas:")
    for nome, qtd in consultas.top_empresas():
        print(f"  {qtd:>3}  {nome}")

    print("\nVagas por estado:")
    for estado, qtd in consultas.vagas_por_estado():
        print(f"  {qtd:>3}  {estado}")

    print("\nÚltimas pesquisas:")
    for cargo, quando in consultas.ultimas_pesquisas():
        print(f"  {quando}  ->  {cargo}")


if __name__ == "__main__":
    main()
