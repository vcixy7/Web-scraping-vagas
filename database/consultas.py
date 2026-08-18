# consultas de leitura no banco, usadas pelo relatório e pela interface
from .db import get_conexao


def total_vagas():
    conexao = get_conexao()
    total = conexao.execute("SELECT COUNT(*) FROM vagas").fetchone()[0]
    conexao.close()
    return total


def total_empresas():
    conexao = get_conexao()
    total = conexao.execute("SELECT COUNT(*) FROM empresas").fetchone()[0]
    conexao.close()
    return total


def salario_medio():
    """Média dos salários que foram encontrados (ignora os vazios). None se não houver."""
    conexao = get_conexao()
    media = conexao.execute("SELECT AVG(salario) FROM vagas WHERE salario IS NOT NULL").fetchone()[0]
    conexao.close()
    return media


def top_empresas(limite=5):
    conexao = get_conexao()
    linhas = conexao.execute(
        """
        SELECT e.nome, COUNT(v.id) AS qtd
        FROM vagas v
        JOIN empresas e ON e.id = v.empresa_id
        GROUP BY e.id
        ORDER BY qtd DESC, e.nome
        LIMIT ?
        """,
        (limite,),
    ).fetchall()
    conexao.close()
    return linhas


def vagas_por_estado():
    conexao = get_conexao()
    linhas = conexao.execute(
        """
        SELECT estado, COUNT(*) AS qtd
        FROM vagas
        GROUP BY estado
        ORDER BY qtd DESC, estado
        """
    ).fetchall()
    conexao.close()
    return linhas


def vagas_por_modalidade():
    conexao = get_conexao()
    linhas = conexao.execute(
        """
        SELECT COALESCE(modalidade, 'Não informado') AS modalidade, COUNT(*) AS qtd
        FROM vagas
        GROUP BY modalidade
        ORDER BY qtd DESC
        """
    ).fetchall()
    conexao.close()
    return linhas


def vagas_por_fonte():
    conexao = get_conexao()
    linhas = conexao.execute(
        """
        SELECT COALESCE(fonte, 'desconhecida') AS fonte, COUNT(*) AS qtd
        FROM vagas
        GROUP BY fonte
        ORDER BY qtd DESC
        """
    ).fetchall()
    conexao.close()
    return linhas


def top_tecnologias(limite=10):
    conexao = get_conexao()
    linhas = conexao.execute(
        """
        SELECT t.nome, COUNT(vt.vaga_id) AS qtd
        FROM tecnologias t
        JOIN vaga_tecnologias vt ON vt.tecnologia_id = t.id
        GROUP BY t.id
        ORDER BY qtd DESC, t.nome
        LIMIT ?
        """,
        (limite,),
    ).fetchall()
    conexao.close()
    return linhas


def vagas_por_dia():
    conexao = get_conexao()
    linhas = conexao.execute(
        """
        SELECT substr(coletada_em, 1, 10) AS dia, COUNT(*) AS qtd
        FROM vagas
        WHERE coletada_em IS NOT NULL
        GROUP BY dia
        ORDER BY dia
        """
    ).fetchall()
    conexao.close()
    return linhas


def historico_pesquisas(limite=15):
    conexao = get_conexao()
    linhas = conexao.execute(
        """
        SELECT id, cargo, criada_em, total_coletadas, novas
        FROM pesquisas
        ORDER BY id DESC
        LIMIT ?
        """,
        (limite,),
    ).fetchall()
    conexao.close()
    return linhas


def vagas_da_pesquisa(pesquisa_id):
    conexao = get_conexao()
    linhas = conexao.execute(
        """
        SELECT v.titulo, e.nome, v.local, v.estado, v.modalidade, v.salario_texto, v.fonte, v.url
        FROM vagas v
        JOIN empresas e ON e.id = v.empresa_id
        WHERE v.pesquisa_id = ?
        ORDER BY v.id
        """,
        (pesquisa_id,),
    ).fetchall()
    conexao.close()
    return linhas
