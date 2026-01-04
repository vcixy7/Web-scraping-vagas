import re

def extrair_estado(local):
    if not local:
        return "Não informado"

    local_up = local.upper()

    # Não retornar "Remoto" — usuário não quer tipo de trabalho
    match = re.search(r"\b[A-Z]{2}\b", local_up)
    if match:
        return match.group()

    return "Não informado"


def _normalize_amount_text(text):
    t = text.strip()
    t = t.replace('R$', '').replace('\xa0', '').strip()
    
    if '.' in t and ',' in t:
        t = t.replace('.', '').replace(',', '.')
    elif ',' in t and '.' not in t:
        t = t.replace(',', '.')
    else:
        
        t = t.replace('.', '')
    try:
        return float(t)
    except:
        return None


def parse_salario(text):
    """Extrai e normaliza um valor médio mensal a partir de um texto de salário.

    Retorna float (valor mensal médio) ou None se não for possível extrair.
    Regras:
    - Captura valores com 'R$' preferencialmente, ou números simples como fallback.
    - Se encontrar um range, calcula a média.
    - Converte anual -> mensal (/12), hora -> mensal (*220), dia -> mensal (*22).
    """
    if not text:
        return None

    txt = text.lower()

    # procurar valores com R$
    amounts = []
    for m in re.findall(r"r\$\s*[\d\.\,]+", txt, flags=re.IGNORECASE):
        n = _normalize_amount_text(m)
        if n is not None:
            amounts.append(n)

    # fallback: buscar números isolados (cautela)
    if not amounts:
        for m in re.findall(r"[\d\.\,]{3,}", txt):
            n = _normalize_amount_text(m)
            if n is not None:
                amounts.append(n)

    if not amounts:
        return None

    avg = sum(amounts) / len(amounts)

    # detectar periodicidade
    if any(x in txt for x in ("ano", "anual", "por ano")):
        avg = avg / 12.0
    elif any(x in txt for x in ("hora", "/h", "por hora")):
        avg = avg * 220.0
    elif any(x in txt for x in ("dia", "por dia")):
        avg = avg * 22.0

    return avg


def format_brl(value):
    """Formata float para string em formato brasileiro com prefixo R$.

    Ex.: 3000.5 -> 'R$ 3.000,50'
    """
    try:
        s = f"{value:,.2f}"
        # s tem formato '3,000.50' em locale C; trocar separadores para BR
        s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"R$ {s}"
    except:
        return "R$ 0,00"
