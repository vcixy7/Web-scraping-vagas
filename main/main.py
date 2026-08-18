import os
import sys

# garante que a raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper.browser import get_browser
from scraper.parser import parse_vagas
from exporter.excel import salvar_excel
from database.db import iniciar_banco, registrar_pesquisa, salvar_vagas, contar_vagas


def main():
    cargo = input("Digite o cargo desejado: ").strip()

    iniciar_banco()
    registrar_pesquisa(cargo)

    url = f"https://br.indeed.com/jobs?q={cargo.replace(' ', '+')}"
    print("\nBuscando vagas...")

    driver = get_browser()
    driver.get(url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    time.sleep(10)

    vagas = parse_vagas(driver)
    driver.quit()

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
