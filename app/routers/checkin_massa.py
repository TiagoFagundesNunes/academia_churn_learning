from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.queue.producer import enviar_checkins_em_lote

router = APIRouter()

class CheckinItem(BaseModel):
    aluno_id: int
    data_hora: str  # pode ser datetime se quiser validar mais estritamente

@router.post("/checkin/massa")
def enviar_checkins_massa(checkins: List[CheckinItem]):
    """
    Envia uma lista de check-ins para a fila RabbitMQ.
    
    Exemplo de corpo da requisição:
    [
        {"aluno_id": 1, "data_hora": "2025-04-06T09:00:00"},
        {"aluno_id": 2, "data_hora": "2025-04-07T14:00:00"}
    ]
    """
    checkins_dict = [checkin.model_dump() for checkin in checkins]  # para Pydantic v2
    enviar_checkins_em_lote(checkins_dict)
    return {"mensagem": "Check-ins enviados para a fila com sucesso"}
