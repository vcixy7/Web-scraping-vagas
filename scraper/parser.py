from selenium.webdriver.common.by import By
from .util import extrair_estado, normalizar_modalidade, parse_salario, format_brl
from .tecnologias import extrair_tecnologias
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
            # texto completo do card, usado para modalidade e tecnologias
            try:
                texto_card = card.text or ""
            except:
                texto_card = ""

            # Título: várias tentativas
            titulo = ""
            try:
                titulo = card.find_element(By.TAG_NAME, "h2").text
            except:
                try:
                    titulo = card.find_element(By.CSS_SELECTOR, ".jobTitle, .job-title, .title").text
                except:
                    linhas = texto_card.split("\n")
                    titulo = linhas[0] if linhas else ""

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
            salario_texto = "Sem informação"
            salario_valor = None
            raw_salario = ""
            for sel in ("[data-testid='attribute_snippet_testid']", ".salary-snippet-container", ".salaryText"):
                try:
                    s = card.find_element(By.CSS_SELECTOR, sel).text
                    if s:
                        raw_salario = s
                        break
                except:
                    continue

            # Se houver números no texto, tentar extrair um valor médio mensal
            if raw_salario and any(ch.isdigit() for ch in raw_salario):
                salario_valor = parse_salario(raw_salario)
                if salario_valor:
                    salario_texto = f"{format_brl(salario_valor)} (médio/mês)"
                else:
                    salario_texto = "Não tem essa informação"

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

            # Modalidade e tecnologias, a partir do que dá para ler no card
            modalidade = normalizar_modalidade(f"{local} {titulo} {texto_card}")
            tecnologias = extrair_tecnologias(f"{titulo} {texto_card}")

            vagas.append({
                "titulo": titulo or "Não informado",
                "empresa": empresa or "Não informado",
                "local": local or "Não informado",
                "estado": extrair_estado(local),
                "modalidade": modalidade,
                "salario": salario_valor,        # valor médio mensal (float) ou None
                "salario_texto": salario_texto,  # versão exibível ("R$ ... (médio/mês)")
                "tecnologias": tecnologias,      # lista de tecnologias encontradas
                "url": link,
            })

        except Exception:
            continue

    return vagas
