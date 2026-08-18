# consultas de leitura no banco, usadas pelo relatório (e depois pela interface)
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


def ultimas_pesquisas(limite=5):
    conexao = get_conexao()
    linhas = conexao.execute(
        "SELECT cargo, criada_em FROM pesquisas ORDER BY id DESC LIMIT ?",
        (limite,),
    ).fetchall()
    conexao.close()
    return linhas
