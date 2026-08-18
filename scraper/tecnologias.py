# identifica tecnologias mencionadas no texto de uma vaga (heurística por palavra)
import re

# lista de tecnologias procuradas (nome como deve aparecer no relatório)
TECNOLOGIAS = [
    "Python", "Java", "JavaScript", "TypeScript", "C#", "C++", "Go", "Ruby",
    "PHP", "Kotlin", "Swift", "Scala", "Rust",
    "SQL", "MySQL", "PostgreSQL", "SQL Server", "Oracle", "MongoDB", "Redis", "SQLite",
    "HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Next.js", "jQuery",
    "Bootstrap", "Tailwind", "Django", "Flask", "FastAPI", "Spring Boot", "Spring",
    ".NET", "Laravel", "Express", "Rails",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Terraform", "Linux", "Git",
    "Jenkins", "Power BI", "Excel", "Tableau", "Pandas", "Spark", "Kafka", "Selenium",
]


def _casa(nome, texto):
    # fronteira que não quebra em símbolos comuns de tecnologias (+ # .)
    padrao = r"(?<![A-Za-z0-9+#.])" + re.escape(nome) + r"(?![A-Za-z0-9+#])"
    return re.search(padrao, texto, re.IGNORECASE) is not None


def extrair_tecnologias(texto):
    """Devolve a lista de tecnologias encontradas no texto (sem repetir)."""
    if not texto:
        return []
    return [nome for nome in TECNOLOGIAS if _casa(nome, texto)]
