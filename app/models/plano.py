from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Plano(Base):
    __tablename__ = 'planos'

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False, unique=True)
    valor = Column(Float, nullable=False)
    duracao_plano = Column(Integer, nullable=False)  # nome atualizado
