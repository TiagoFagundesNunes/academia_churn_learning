from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from app.database import SessionLocal
from app.models.checkin import Checkin
from app.models.aluno import Aluno
from app.schemas.checkin import CheckinCreate, CheckinInfo

router = APIRouter()

# Dependência de sessão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 📌 Rota de Check-in
@router.post("/checkin", status_code=status.HTTP_201_CREATED)
def registrar_checkin(checkin: CheckinCreate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == checkin.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    checkin_em_aberto = (
        db.query(Checkin)
        .filter(Checkin.aluno_id == checkin.aluno_id, Checkin.data_saida == None)
        .first()
    )

    # Se já existe check-in em aberto, ignora a tentativa e retorna a mensagem
    if checkin_em_aberto:
        return {
            "mensagem": "Check-in ignorado (já existe um em andamento)",
            "id": checkin_em_aberto.id
        }

    novo_checkin = Checkin(
        aluno_id=checkin.aluno_id,
        data_hora=checkin.data_hora
    )
    db.add(novo_checkin)
    db.commit()
    db.refresh(novo_checkin)
    return {"mensagem": "Check-in registrado com sucesso", "id": novo_checkin.id}

# ✅ Rota de Checkout
@router.post("/checkout", status_code=status.HTTP_200_OK)
def registrar_checkout(aluno_id: int, db: Session = Depends(get_db)):
    checkin = db.query(Checkin).filter(
        Checkin.aluno_id == aluno_id,
        Checkin.data_saida.is_(None)
    ).order_by(Checkin.data_hora.desc()).first()

    if not checkin:
        raise HTTPException(status_code=404, detail="Nenhum check-in pendente encontrado para esse aluno.")

    agora = datetime.utcnow()
    limite = checkin.data_hora + timedelta(hours=5)
    checkin.data_saida = min(agora, limite)

    checkin.calcular_duracao()
    db.commit()
    db.refresh(checkin)

    return {
        "mensagem": "Checkout registrado com sucesso",
        "aluno_id": aluno_id,
        "duracao_minutos": checkin.duracao,
        "entrada": checkin.data_hora,
        "saida": checkin.data_saida
    }

# 📌 Rota de Frequência
@router.get("/{aluno_id}/frequencia", response_model=List[CheckinInfo])
def listar_frequencia(aluno_id: int, db: Session = Depends(get_db)):
    checkins = db.query(Checkin).filter(Checkin.aluno_id == aluno_id).order_by(Checkin.data_hora).all()

    if not checkins:
        raise HTTPException(status_code=404, detail="Nenhum check-in encontrado para esse aluno.")
    
    return checkins