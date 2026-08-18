# fonte Remotive (API pública, sem chave): vagas remotas, boa para tecnologia
import requests
from .comum import montar_vaga

NOME = "remotive"
URL = "https://remotive.com/api/remote-jobs"


def coletar(cargo, limite=30):
    resposta = requests.get(URL, params={"search": cargo, "limit": limite}, timeout=20)
    resposta.raise_for_status()
    jobs = resposta.json().get("jobs", [])

    vagas = []
    for job in jobs[:limite]:
        tags = " ".join(job.get("tags", []) or [])
        texto = f"{job.get('description', '')} {tags}"
        vagas.append(montar_vaga(
            titulo=job.get("title"),
            empresa=job.get("company_name"),
            local=job.get("candidate_required_location") or "Remoto",
            url=job.get("url"),
            fonte=NOME,
            texto_para_tec=texto,
            salario_texto=job.get("salary") or None,
        ))
    return vagas
