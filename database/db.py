# camada de persistência: guarda as vagas coletadas em um banco SQLite
import os
import sqlite3
from datetime import datetime

# o banco fica em data/vagas.db, na raiz do projeto
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_BANCO = os.path.join(RAIZ, "data", "vagas.db")


def get_conexao():
    os.makedirs(os.path.dirname(CAMINHO_BANCO), exist_ok=True)
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def iniciar_banco():
    """Cria as tabelas caso ainda não existam."""
    conexao = get_conexao()
    conexao.executescript(
        """
        CREATE TABLE IF NOT EXISTS empresas (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS vagas (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo        TEXT,
            empresa_id    INTEGER REFERENCES empresas(id),
            local         TEXT,
            estado        TEXT,
            salario       REAL,
            salario_texto TEXT,
            url           TEXT UNIQUE,
            coletada_em   TEXT
        );

        CREATE TABLE IF NOT EXISTS pesquisas (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            cargo     TEXT,
            criada_em TEXT
        );
        """
    )
    conexao.commit()
    conexao.close()


def _obter_ou_criar_empresa(cursor, nome):
    cursor.execute("INSERT OR IGNORE INTO empresas (nome) VALUES (?)", (nome,))
    cursor.execute("SELECT id FROM empresas WHERE nome = ?", (nome,))
    return cursor.fetchone()[0]


def salvar_vagas(vagas):
    """Salva as vagas no banco, ignorando as que já existem (mesma URL).

    Retorna uma tupla (novas, duplicadas).
    """
    conexao = get_conexao()
    cursor = conexao.cursor()
    novas = 0
    duplicadas = 0

    for vaga in vagas:
        empresa_id = _obter_ou_criar_empresa(cursor, vaga.get("empresa") or "Não informado")

        url = vaga.get("url")
        if not url or url == "Não disponível":
            # sem URL não dá para identificar duplicata; deixa NULL para não colidir
            url = None

        cursor.execute(
            """
            INSERT OR IGNORE INTO vagas
                (titulo, empresa_id, local, estado, salario, salario_texto, url, coletada_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                vaga.get("titulo"),
                empresa_id,
                vaga.get("local"),
                vaga.get("estado"),
                vaga.get("salario"),
                vaga.get("salario_texto"),
                url,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        # rowcount == 1 quando inseriu; 0 quando ignorou (URL repetida)
        if cursor.rowcount == 1:
            novas += 1
        else:
            duplicadas += 1

    conexao.commit()
    conexao.close()
    return novas, duplicadas


def registrar_pesquisa(cargo):
    """Guarda o cargo pesquisado, para montar um histórico depois."""
    conexao = get_conexao()
    conexao.execute(
        "INSERT INTO pesquisas (cargo, criada_em) VALUES (?, ?)",
        (cargo, datetime.now().isoformat(timespec="seconds")),
    )
    conexao.commit()
    conexao.close()


def contar_vagas():
    conexao = get_conexao()
    total = conexao.execute("SELECT COUNT(*) FROM vagas").fetchone()[0]
    conexao.close()
    return total
