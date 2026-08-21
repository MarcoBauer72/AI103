import mermaid as md
from mermaid.graph import Graph

# Definir a estrutura do diagrama Mermaid
conteudo_mmd = """
graph TD
    A[Início] --> B{Validar}
    B -- Sim --> C[Sucesso]
    B -- Não --> D[Erro]
"""

# Gravar o ficheiro MMD
with open("diagrama.mmd", "w", encoding="utf-8") as f:
    f.write(conteudo_mmd.strip())

print("Ficheiro diagrama.mmd gerado com sucesso!")