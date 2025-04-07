from pydantic import BaseModel
from datetime import date

# Info sobre o plano (resposta)
class PlanoInfo(BaseModel):
    tipo: str
    valor: float
    duracao_plano: int

    class Config:
        from_attributes = True

# Envio ao criar contrato
class ContratoCreate(BaseModel):
    aluno_id: int
    plano_id: int
    data_inicio: date
    duracao_meses: int  # usado para calcular data_fim

# Retorno com detalhes
class ContratoInfo(BaseModel):
    id: int
    aluno_id: int
    plano: PlanoInfo
    data_inicio: date
    data_fim: date
    ativo: bool

    class Config:
        from_attributes = True
