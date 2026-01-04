import os
import sys

# Garantir que o diretório raiz do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.browser import get_browser
from scraper.parser import parse_vagas
from exporter.excel import salvar_excel
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    cargo = input("Digite o cargo desejado: ").strip()

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

    salvar_excel(vagas)
    print(f"{len(vagas)} vagas salvas no arquivo vagas.xlsx")

if __name__ == "__main__":
    main()
