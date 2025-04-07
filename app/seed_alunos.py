from app.database import SessionLocal
from app.models.aluno import Aluno
import pandas as pd
from datetime import datetime

db = SessionLocal()

# Lê o CSV
df = pd.read_csv("data/dados_alunos.csv")
df["data_nascimento"] = pd.to_datetime(df["data_nascimento"]).dt.date

inseridos = 0

for _, row in df.iterrows():
    # Verifica se já existe
    existe = db.query(Aluno).filter(Aluno.id == row["id"]).first()
    if existe:
        continue

    aluno = Aluno(
        id=int(row["id"]),
        nome=row["nome"],
        cpf=row["cpf"],
        genero=row["genero"],
        data_nascimento=row["data_nascimento"]
    )

    db.add(aluno)
    inseridos += 1

db.commit()
db.close()
print(f"✅ {inseridos} alunos foram inseridos no banco de dados.")
