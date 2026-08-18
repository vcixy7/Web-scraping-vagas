# helper compartilhado: monta uma vaga no formato padrão do projeto,
# já normalizando modalidade/UF e extraindo as tecnologias do texto.
from scraper.util import extrair_estado, normalizar_modalidade, format_brl
from scraper.tecnologias import extrair_tecnologias


def montar_vaga(titulo, empresa, local, url, fonte, texto_para_tec="", salario_texto=None, salario=None):
    if salario is not None:
        exibivel = f"{format_brl(salario)} (médio/mês)"
    elif salario_texto:
        exibivel = salario_texto
    else:
        exibivel = "Sem informação"

    titulo = (titulo or "").strip() or "Não informado"
    empresa = (empresa or "").strip() or "Não informado"
    local = (local or "").strip() or "Não informado"

    return {
        "titulo": titulo,
        "empresa": empresa,
        "local": local,
        "estado": extrair_estado(local),
        "modalidade": normalizar_modalidade(f"{local} {titulo} {texto_para_tec}"),
        "salario": salario,
        "salario_texto": exibivel,
        "tecnologias": extrair_tecnologias(f"{titulo} {texto_para_tec}"),
        "url": (url or "").strip() or "Não disponível",
        "fonte": fonte,
    }
