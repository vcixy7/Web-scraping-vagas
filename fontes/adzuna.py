# fonte Adzuna (API oficial): cobertura ampla, inclusive Brasil.
# Só funciona se você configurar as chaves grátis nas variáveis de ambiente:
#   ADZUNA_APP_ID e ADZUNA_APP_KEY  (crie em https://developer.adzuna.com/)
#   ADZUNA_PAIS (opcional, padrão "br")
import os
import requests
from .comum import montar_vaga

NOME = "adzuna"


def coletar(cargo, limite=30):
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    if not app_id or not app_key:
        # fonte opcional: sem chaves, simplesmente não coleta
        return []

    pais = os.getenv("ADZUNA_PAIS", "br")
    url = f"https://api.adzuna.com/v1/api/jobs/{pais}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": cargo,
        "results_per_page": limite,
        "content-type": "application/json",
    }

    resposta = requests.get(url, params=params, timeout=20)
    resposta.raise_for_status()
    resultados = resposta.json().get("results", [])

    vagas = []
    for job in resultados[:limite]:
        empresa = (job.get("company") or {}).get("display_name")
        local = (job.get("location") or {}).get("display_name")

        smin, smax = job.get("salary_min"), job.get("salary_max")
        salario_texto = None
        if smin or smax:
            salario_texto = f"{smin or ''} - {smax or ''}".strip(" -")

        vagas.append(montar_vaga(
            titulo=job.get("title"),
            empresa=empresa,
            local=local,
            url=job.get("redirect_url"),
            fonte=NOME,
            texto_para_tec=job.get("description", ""),
            salario_texto=salario_texto,
        ))
    return vagas
