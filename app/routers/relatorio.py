from fastapi import APIRouter
from app.queue.producer_relatorio import solicitar_relatorio_diario

router = APIRouter()

@router.post("/relatorio/diario")
def gerar_relatorio():
    solicitar_relatorio_diario()
    return {"mensagem": "Solicitação de relatório enviada para a fila"}
