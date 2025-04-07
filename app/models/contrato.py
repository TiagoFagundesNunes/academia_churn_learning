from sqlalchemy import Column, Integer, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.plano import Plano
from app.models.aluno import Aluno

class Contrato(Base):
    __tablename__ = 'contratos'

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'), nullable=False)
    plano_id = Column(Integer, ForeignKey('planos.id'), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    ativo = Column(Boolean, default=True)

    aluno = relationship("Aluno", backref="contratos")
    plano = relationship("Plano", backref="contratos")
