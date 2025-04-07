from pydantic import BaseModel, constr
from datetime import date

class AlunoCreate(BaseModel):
    nome: constr(strip_whitespace=True, min_length=1)
    cpf: constr(min_length=11, max_length=11)
    genero: constr(min_length=1, max_length=1)
    data_nascimento: date
    senha: constr(min_length=4)
