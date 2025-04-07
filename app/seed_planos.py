from app.database import SessionLocal
from app.models.plano import Plano

db = SessionLocal()

# Valores e alterações de planos
novos_planos = [
    {"tipo": "Silver", "valor": 150.00, "duracao_meses": 1},
    {"tipo": "Gold", "valor": 130.00, "duracao_meses": 3},
    {"tipo": "Premium", "valor": 110.00, "duracao_meses": 12},
]

for plano_data in novos_planos:
    plano = db.query(Plano).filter(Plano.tipo == plano_data["tipo"]).first()

    if plano:
        # Atualiza planos existentes
        plano.valor = plano_data["valor"]
        plano.duracao_meses = plano_data["duracao_meses"]
        print(f"🔄 Plano '{plano.tipo}' atualizado.")
    else:
        # Cria novo se n existir
        novo_plano = Plano(**plano_data)
        db.add(novo_plano)
        print(f"✅ Plano '{plano_data['tipo']}' criado.")

db.commit()
db.close()
print("...Atualização dos planos concluída.")

#atualizar planos -> python -m app.seed_planos