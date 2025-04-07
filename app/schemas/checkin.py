from pydantic import BaseModel
from datetime import datetime

class CheckinCreate(BaseModel):
    aluno_id: int
    data_hora: datetime

class CheckinInfo(BaseModel):
    id: int
    data_hora: datetime
    data_saida: datetime | None
    duracao: int

    class Config:
        from_attributes = True