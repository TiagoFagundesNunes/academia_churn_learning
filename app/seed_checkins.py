from app.database import SessionLocal
from app.models.checkin import Checkin
from app.models.aluno import Aluno  # ✅ ADICIONAR ISSO
from datetime import datetime, timedelta
import random
import pandas as pd

# Lê os dados dos alunos simulados
df_alunos = pd.read_csv("data/dados_alunos.csv")
df_alunos["data_inicio"] = pd.to_datetime(df_alunos["data_inicio"])

db = SessionLocal()

total_inseridos = 0

for _, aluno in df_alunos.iterrows():
    aluno_id = aluno["id"]
    data_inicio = aluno["data_inicio"]
    num_checkins = random.randint(5, 25)

    for _ in range(num_checkins):
        dias_offset = random.randint(0, (datetime.now() - data_inicio).days)
        data_hora = (data_inicio + timedelta(days=dias_offset)).replace(
            hour=random.randint(6, 20), minute=0, second=0
        )

        duracao_minutos = random.randint(30, 300)
        data_saida = data_hora + timedelta(minutes=duracao_minutos)

        checkin = Checkin(
            aluno_id=aluno_id,
            data_hora=data_hora,
            data_saida=data_saida
        )
        checkin.calcular_duracao()
        db.add(checkin)
        total_inseridos += 1

db.commit()
db.close()
print(f"✅ {total_inseridos} check-ins realistas foram adicionados ao banco!")
