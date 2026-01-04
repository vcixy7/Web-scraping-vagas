from selenium.webdriver.common.by import By
from .util import extrair_estado, parse_salario, format_brl
import time

def parse_vagas(driver):
    vagas = []

    selector_candidates = [
        (By.TAG_NAME, "article"),
        (By.CSS_SELECTOR, "a.tapItem"),
        (By.CSS_SELECTOR, "div.job_seen_beacon"),
        (By.CSS_SELECTOR, "div.jobsearch-SerpJobCard"),
        (By.CSS_SELECTOR, "div.slider_item"),
    ]

    cards = []
    for by, sel in selector_candidates:
        try:
            found = driver.find_elements(by, sel)
            if found:
                print(f"{len(found)} cards encontrados com selector {sel}")
                cards = found
                break
        except Exception as e:
            print(f"Erro ao usar selector {sel}: {e}")

    if not cards:
        # última tentativa: buscar por links que costumam envolver vagas
        try:
            found = driver.find_elements(By.CSS_SELECTOR, "a[href*='/rc/clk']")
            if found:
                print(f"{len(found)} cards encontrados com fallback a[href*='/rc/clk']")
                cards = found
        except Exception as e:
            print(f"Erro no fallback: {e}")

    print(f"Total de cards a processar: {len(cards)}")

    for card in cards:
        try:
            # Título: várias tentativas
            titulo = ""
            try:
                titulo = card.find_element(By.TAG_NAME, "h2").text
            except:
                try:
                    titulo = card.find_element(By.CSS_SELECTOR, ".jobTitle, .job-title, .title").text
                except:
                    texto = card.text.split("\n")
                    titulo = texto[0] if texto else ""

            # Empresa: tentativas com seletores comuns
            empresa = ""
            for sel in ("[data-testid='company-name']", ".companyName", ".company", ".icl-u-lg-mr--sm"):
                try:
                    empresa = card.find_element(By.CSS_SELECTOR, sel).text
                    if empresa:
                        break
                except:
                    continue

            # Local
            local = ""
            for sel in ("[data-testid='text-location']", ".companyLocation", ".location"):
                try:
                    local = card.find_element(By.CSS_SELECTOR, sel).text
                    if local:
                        break
                except:
                    continue

            # Salário
            salario = "Sem informação"
            raw_salario = ""
            for sel in ("[data-testid='attribute_snippet_testid']", ".salary-snippet-container", ".salaryText"):
                try:
                    s = card.find_element(By.CSS_SELECTOR, sel).text
                    if s:
                        raw_salario = s
                        break
                except:
                    continue

            # Se houver números no texto, tentar parsear e calcular valor médio mensal
            if raw_salario and any(ch.isdigit() for ch in raw_salario):
                avg = parse_salario(raw_salario)
                if avg:
                    salario = f"{format_brl(avg)} (médio/mês)"
                else:
                    salario = "Não tem essa informação"

            # Link da vaga
            link = ""
            try:
                link = card.get_attribute('href') or ""
            except:
                link = ""

            if not link:
                try:
                    a = card.find_element(By.CSS_SELECTOR, "a")
                    link = a.get_attribute('href') or ""
                except:
                    link = ""

            if not link:
                link = "Não disponível"

            vagas.append({
                "Título": titulo or "Não informado",
                "Empresa": empresa or "Não informado",
                "Local": local or "Não informado",
                "Estado (UF)": extrair_estado(local),
                "Salário": salario,
                "Link": link,
            })

        except Exception:
            continue

    return vagas
