# fontes de vagas: cada módulo sabe coletar de um site/serviço e devolver as
# vagas no mesmo formato. Assim dá para caçar em vários lugares de uma vez.
from . import indeed, remotive, remoteok, adzuna

FONTES = {
    indeed.NOME: indeed,
    remotive.NOME: remotive,
    remoteok.NOME: remoteok,
    adzuna.NOME: adzuna,
}


def nomes():
    return list(FONTES.keys())


def coletar_de(cargo, nomes_fontes, limite=30):
    """Coleta nas fontes escolhidas e junta tudo.

    Uma fonte que falhar (rede, mudança na API) não derruba as outras.
    """
    vagas = []
    for nome in nomes_fontes:
        fonte = FONTES.get(nome)
        if fonte is None:
            print(f"[aviso] fonte desconhecida: {nome}")
            continue
        try:
            encontradas = fonte.coletar(cargo, limite=limite)
            print(f"[{nome}] {len(encontradas)} vagas")
            vagas.extend(encontradas)
        except Exception as e:
            print(f"[{nome}] erro na coleta: {e}")
    return vagas
