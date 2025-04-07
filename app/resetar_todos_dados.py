from app.database import SessionLocal, engine
from sqlalchemy import text

db = SessionLocal()

# Apaga os dados das tabelas respeitando a ordem de chaves estrangeiras
db.execute(text("DELETE FROM checkins"))
db.execute(text("DELETE FROM contratos"))
db.execute(text("DELETE FROM alunos"))

# Reseta os IDs (sequences)
db.execute(text("ALTER SEQUENCE checkins_id_seq RESTART WITH 1"))
db.execute(text("ALTER SEQUENCE contratos_id_seq RESTART WITH 1"))
db.execute(text("ALTER SEQUENCE alunos_id_seq RESTART WITH 1"))

db.commit()
db.close()

print("🔁 Dados apagados e contadores resetados.")

#python resetar_todos_dados.py