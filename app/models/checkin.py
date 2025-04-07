from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.database import Base

class Checkin(Base):
    __tablename__ = 'checkins'

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'), nullable=False)
    data_hora = Column(DateTime, nullable=False, default=datetime.utcnow)  # entrada
    data_saida = Column(DateTime, nullable=True)  # saída
    duracao = Column(Integer, nullable=False, default=0)  # em minutos

    from app.models.aluno import Aluno
    aluno = relationship(Aluno)


    def calcular_duracao(self):
        if self.data_saida:
            delta = self.data_saida - self.data_hora
            minutos = int(delta.total_seconds() // 60)
            self.duracao = min(minutos, 300)  # máximo 5h = 300min
        else:
            self.duracao = 0
