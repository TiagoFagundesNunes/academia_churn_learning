from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import SessionLocal
from app.models.contrato import Contrato
from app.models.plano import Plano
from app.schemas.contrato import ContratoCreate, ContratoInfo

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET existente
@router.get("/contrato/{contrato_id}", response_model=ContratoInfo)
def get_contrato(contrato_id: int, db: Session = Depends(get_db)):
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
    return contrato

# ✅ NOVO POST
@router.post("/contrato", response_model=ContratoInfo, status_code=status.HTTP_201_CREATED)
def criar_contrato(contrato: ContratoCreate, db: Session = Depends(get_db)):
    plano = db.query(Plano).filter(Plano.id == contrato.plano_id).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    data_fim = contrato.data_inicio + timedelta(days=contrato.duracao_meses * 30)

    novo_contrato = Contrato(
        aluno_id=contrato.aluno_id,
        plano_id=contrato.plano_id,
        data_inicio=contrato.data_inicio,
        data_fim=data_fim,
        ativo=True
    )
    db.add(novo_contrato)
    db.commit()
    db.refresh(novo_contrato)
    return novo_contrato
