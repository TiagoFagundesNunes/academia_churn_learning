from app.database import SessionLocal
from app.models.aluno import Aluno
from app.models.checkin import Checkin
from app.models.contrato import Contrato

db = SessionLocal()

# Alunos considerados simulados: ids de 1 a 50
alunos_simulados = db.query(Aluno).filter(Aluno.id <= 50).all()
ids_simulados = [aluno.id for aluno in alunos_simulados]

# Remove check-ins desses alunos
checkins_deletados = db.query(Checkin).filter(Checkin.aluno_id.in_(ids_simulados)).delete(synchronize_session=False)

# Remove contratos desses alunos
contratos_deletados = db.query(Contrato).filter(Contrato.aluno_id.in_(ids_simulados)).delete(synchronize_session=False)

# Remove os próprios alunos
alunos_deletados = db.query(Aluno).filter(Aluno.id.in_(ids_simulados)).delete(synchronize_session=False)

db.commit()
db.close()

print(f"🧹 Alunos removidos: {len(ids_simulados)}")
print(f"🧹 Check-ins removidos: {checkins_deletados}")
print(f"🧹 Contratos removidos: {contratos_deletados}")
