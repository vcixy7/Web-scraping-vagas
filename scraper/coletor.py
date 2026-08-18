# junta o navegador + o parser: abre a busca e devolve as vagas encontradas
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .browser import get_browser
from .parser import parse_vagas


def coletar(cargo):
    """Abre o Indeed, pesquisa pelo cargo informado e devolve a lista de vagas."""
    url = f"https://br.indeed.com/jobs?q={cargo.replace(' ', '+')}"

    driver = get_browser()
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(10)  # dá um tempo para a página carregar os cards
        return parse_vagas(driver)
    finally:
        driver.quit()
