from app.database import SessionLocal
from app.models.contrato import Contrato
from app.models.plano import Plano
from datetime import datetime, timedelta
import random

db = SessionLocal()

# Recupera todos os planos do banco
planos = db.query(Plano).all()
planos_por_tipo = {plano.tipo: plano for plano in planos}

# Dicionário para facilitar a escolha aleatória
planos_disponiveis = list(planos_por_tipo.values())

# Para cada aluno, cria um contrato
for aluno_id in range(1, 51):
    plano = random.choice(planos_disponiveis)
    data_inicio = datetime.now() - timedelta(days=random.randint(10, 120))
    data_fim = data_inicio + timedelta(days=plano.duracao_plano * 30)

    contrato = Contrato(
        aluno_id=aluno_id,
        plano_id=plano.id,
        data_inicio=data_inicio.date(),
        data_fim=data_fim.date(),
        ativo=True
    )

    db.add(contrato)
    print(f"✅ Contrato criado para aluno {aluno_id} com plano {plano.tipo}.")

db.commit()
db.close()
print("🎉 Todos os contratos foram criados com sucesso.")
