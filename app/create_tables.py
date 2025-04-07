from app.database import engine, Base
from app.models.aluno import Aluno
from app.models.checkin import Checkin
from app.models.contrato import Contrato
from app.models.plano import Plano

print("Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas.")
