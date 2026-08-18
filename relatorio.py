import os
import sys

# garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db import iniciar_banco
from database import consultas
from scraper.util import format_brl


def _lista(titulo, linhas, vazio="(sem dados)"):
    print(f"\n{titulo}:")
    if not linhas:
        print(f"  {vazio}")
        return
    for nome, qtd in linhas:
        print(f"  {qtd:>3}  {nome}")


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

    _lista("Empresas com mais vagas", consultas.top_empresas())
    _lista("Vagas por estado", consultas.vagas_por_estado())
    _lista("Vagas por modalidade", consultas.vagas_por_modalidade())
    _lista("Tecnologias mais pedidas", consultas.top_tecnologias())
    _lista("Vagas coletadas por dia", consultas.vagas_por_dia())

    print("\nHistórico de pesquisas:")
    historico = consultas.historico_pesquisas()
    if not historico:
        print("  (sem dados)")
    for _id, cargo, quando, total, novas in historico:
        total = total if total is not None else "?"
        novas = novas if novas is not None else "?"
        print(f"  {quando}  ->  {cargo}  ({total} coletadas, {novas} novas)")


if __name__ == "__main__":
    main()
