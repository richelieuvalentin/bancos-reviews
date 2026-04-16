import os

def criar_estrutura_projeto():
    # Como a pasta principal já existe, criamos as subpastas no diretório atual
    pastas = [
        "data/raw",
        "data/processed",
        "data/final",
        "notebooks",
        "src",
        "models",
        "app",
    ]
    
    # Arquivos iniciais com a nova nomenclatura
    arquivos = {
        "src/scraper.py": "# Código do scraper com filtro 2025\n",
        "src/preprocessing.py": "# Funções de limpeza de texto\n",
        "app/main.py": "import streamlit as st\n\nst.title('Dashboard de Sentimento - Bancos Reviews 2025')\n",
        "requirements.txt": "pandas\ngoogle-play-scraper\nstreamlit\nscikit-learn\nlabel-studio\n",
        "README.md": "# Bancos Reviews\nProjeto de análise de sentimento dos grandes bancos brasileiros (Dados de 2025).\n",
        ".gitignore": "data/\nmodels/*.pkl\n__pycache__/\nvenv/\n.env\n"
    }

    print("Ajustando estrutura em: Bancos Reviews")

    # Criando as subpastas
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
        print(f"Pasta garantida: {pasta}")

    # Criando os arquivos (sem sobrescrever se você já tiver algo importante)
    for caminho_arquivo, conteudo in arquivos.items():
        if not os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"Arquivo criado: {caminho_arquivo}")
        else:
            print(f"Arquivo já existe, pulado: {caminho_arquivo}")

    print("\nEstrutura atualizada!")

if __name__ == "__main__":
    criar_estrutura_projeto()