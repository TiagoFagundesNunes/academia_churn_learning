import pandas as pd

# Caminhos relativos dos arquivos
caminho_alunos = "data/base_de_alunos_gerada.csv"
caminho_churn = "data/alunos_gerados_para_churn.csv"

# Lê os arquivos
alunos_df = pd.read_csv(caminho_alunos)
churn_df = pd.read_csv(caminho_churn)

# Mostra as primeiras linhas de cada um
print("📄 Base de alunos:")
print(alunos_df.head())

print("\n📄 Dados de churn:")
print(churn_df.head())
