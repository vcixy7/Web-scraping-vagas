# fonte Indeed: reaproveita o coletor com Selenium que já existia
from scraper.coletor import coletar as _coletar_indeed

NOME = "indeed"


def coletar(cargo, limite=30):
    vagas = _coletar_indeed(cargo)
    for vaga in vagas:
        vaga["fonte"] = NOME
    return vagas[:limite] if limite else vagas
