from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    genero = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    senha = Column(String, nullable=False)
