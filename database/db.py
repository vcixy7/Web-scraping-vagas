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


def _coluna_existe(conexao, tabela, coluna):
    return any(linha[1] == coluna for linha in conexao.execute(f"PRAGMA table_info({tabela})"))


def _migrar(conexao):
    """Adiciona colunas novas em bancos que já existiam antes destas mudanças."""
    novas_colunas = [
        ("vagas", "modalidade", "TEXT"),
        ("vagas", "fonte", "TEXT"),
        ("vagas", "pesquisa_id", "INTEGER"),
        ("pesquisas", "total_coletadas", "INTEGER"),
        ("pesquisas", "novas", "INTEGER"),
    ]
    for tabela, coluna, tipo in novas_colunas:
        if not _coluna_existe(conexao, tabela, coluna):
            conexao.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo}")


def iniciar_banco():
    """Cria as tabelas caso ainda não existam (e migra bancos antigos)."""
    conexao = get_conexao()
    conexao.executescript(
        """
        CREATE TABLE IF NOT EXISTS empresas (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS pesquisas (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            cargo           TEXT,
            criada_em       TEXT,
            total_coletadas INTEGER,
            novas           INTEGER
        );

        CREATE TABLE IF NOT EXISTS vagas (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo        TEXT,
            empresa_id    INTEGER REFERENCES empresas(id),
            local         TEXT,
            estado        TEXT,
            modalidade    TEXT,
            salario       REAL,
            salario_texto TEXT,
            url           TEXT UNIQUE,
            fonte         TEXT,
            coletada_em   TEXT,
            pesquisa_id   INTEGER REFERENCES pesquisas(id)
        );

        CREATE TABLE IF NOT EXISTS tecnologias (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS vaga_tecnologias (
            vaga_id       INTEGER REFERENCES vagas(id),
            tecnologia_id INTEGER REFERENCES tecnologias(id),
            PRIMARY KEY (vaga_id, tecnologia_id)
        );
        """
    )
    _migrar(conexao)
    conexao.commit()
    conexao.close()


def _obter_ou_criar(cursor, tabela, nome):
    cursor.execute(f"INSERT OR IGNORE INTO {tabela} (nome) VALUES (?)", (nome,))
    cursor.execute(f"SELECT id FROM {tabela} WHERE nome = ?", (nome,))
    return cursor.fetchone()[0]


def registrar_pesquisa(cargo):
    """Cria o registro da pesquisa e devolve o id (para ligar às vagas depois)."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO pesquisas (cargo, criada_em) VALUES (?, ?)",
        (cargo, datetime.now().isoformat(timespec="seconds")),
    )
    pesquisa_id = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return pesquisa_id


def salvar_vagas(vagas, pesquisa_id=None):
    """Salva as vagas no banco, ignorando as que já existem (mesma URL).

    Também liga cada vaga nova às suas tecnologias. Retorna (novas, duplicadas).
    """
    conexao = get_conexao()
    cursor = conexao.cursor()
    novas = 0
    duplicadas = 0

    for vaga in vagas:
        empresa_id = _obter_ou_criar(cursor, "empresas", vaga.get("empresa") or "Não informado")

        url = vaga.get("url")
        if not url or url == "Não disponível":
            # sem URL não dá para identificar duplicata; deixa NULL para não colidir
            url = None

        cursor.execute(
            """
            INSERT OR IGNORE INTO vagas
                (titulo, empresa_id, local, estado, modalidade, salario, salario_texto, url, fonte, coletada_em, pesquisa_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                vaga.get("titulo"),
                empresa_id,
                vaga.get("local"),
                vaga.get("estado"),
                vaga.get("modalidade"),
                vaga.get("salario"),
                vaga.get("salario_texto"),
                url,
                vaga.get("fonte"),
                datetime.now().isoformat(timespec="seconds"),
                pesquisa_id,
            ),
        )

        # rowcount == 1 quando inseriu; 0 quando ignorou (URL repetida)
        if cursor.rowcount == 1:
            novas += 1
            vaga_id = cursor.lastrowid
            for tecnologia in vaga.get("tecnologias", []):
                tecnologia_id = _obter_ou_criar(cursor, "tecnologias", tecnologia)
                cursor.execute(
                    "INSERT OR IGNORE INTO vaga_tecnologias (vaga_id, tecnologia_id) VALUES (?, ?)",
                    (vaga_id, tecnologia_id),
                )
        else:
            duplicadas += 1

    if pesquisa_id is not None:
        cursor.execute(
            "UPDATE pesquisas SET total_coletadas = ?, novas = ? WHERE id = ?",
            (len(vagas), novas, pesquisa_id),
        )

    conexao.commit()
    conexao.close()
    return novas, duplicadas


def contar_vagas():
    conexao = get_conexao()
    total = conexao.execute("SELECT COUNT(*) FROM vagas").fetchone()[0]
    conexao.close()
    return total
