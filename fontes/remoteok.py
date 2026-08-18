# fonte RemoteOK (API pública, sem chave): vagas remotas de tecnologia.
# A API devolve todas as vagas; filtramos pelo cargo aqui mesmo.
import requests
from .comum import montar_vaga

NOME = "remoteok"
URL = "https://remoteok.com/api"


def coletar(cargo, limite=30):
    resposta = requests.get(URL, headers={"User-Agent": "coleta-vagas (projeto de estudo)"}, timeout=20)
    resposta.raise_for_status()
    dados = resposta.json()

    # o primeiro item costuma ser um aviso legal, não uma vaga
    if dados and isinstance(dados[0], dict) and dados[0].get("legal"):
        dados = dados[1:]

    termo = (cargo or "").lower().strip()
    vagas = []
    for job in dados:
        if not isinstance(job, dict):
            continue
        tags = " ".join(job.get("tags", []) or [])
        blob = f"{job.get('position', '')} {job.get('description', '')} {tags}".lower()
        if termo and termo not in blob:
            continue

        vagas.append(montar_vaga(
            titulo=job.get("position"),
            empresa=job.get("company"),
            local=job.get("location") or "Remoto",
            url=job.get("url"),
            fonte=NOME,
            texto_para_tec=f"{job.get('description', '')} {tags}",
        ))
        if len(vagas) >= limite:
            break
    return vagas
