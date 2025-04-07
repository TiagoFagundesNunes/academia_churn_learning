from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import pandas as pd

from app.database import SessionLocal
from app.models.aluno import Aluno
from app.schemas.aluno import AlunoCreate
from app.auth import (
    get_current_user,
    gerar_hash,
    verificar_senha,
    criar_token
)
from app.services.churn_model import (
    calcular_risco_churn,
    calcular_risco_churn_completo
)

router = APIRouter()

# Carrega os dados do churn completo apenas uma vez
dados_csv = pd.read_csv("data/dados_churn.csv")

# Dependência de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔐 Registro de novo aluno
@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    if db.query(Aluno).filter(Aluno.cpf == aluno.cpf).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado."
        )
    
    senha_hash = gerar_hash(aluno.senha)
    novo_aluno = Aluno(
        nome=aluno.nome,
        cpf=aluno.cpf,
        genero=aluno.genero,
        data_nascimento=aluno.data_nascimento,
        senha=senha_hash
    )

    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return {"mensagem": "Aluno cadastrado com sucesso", "id": novo_aluno.id}

# 🔑 Login e geração de token JWT
@router.post("/login")
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        print("Tentando login com:", form_data.username)
        aluno = db.query(Aluno).filter(Aluno.cpf == form_data.username).first()
        print("Aluno encontrado:", aluno)

        if not aluno or not verificar_senha(form_data.password, aluno.senha):
            print("Senha incorreta ou aluno não encontrado")
            raise HTTPException(status_code=400, detail="CPF ou senha incorretos")

        access_token = criar_token(data={"sub": str(aluno.id)})
        print("Token gerado:", access_token)
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print("Erro inesperado no login:", e)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

# 📊 Previsão de churn (modelo básico)
@router.get("/{aluno_id}/risco-churn")
def risco_churn(
    aluno_id: int,
    db: Session = Depends(get_db),
    usuario_logado=Depends(get_current_user)
):
    if not db.query(Aluno).filter(Aluno.id == aluno_id).first():
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    risco = calcular_risco_churn(aluno_id, db)
    return {"aluno_id": aluno_id, "risco_churn": risco}

# 📈 Previsão de churn (modelo completo)
@router.get("/{aluno_id}/risco-churn/completo")
def risco_churn_completo(
    aluno_id: int,
    db: Session = Depends(get_db),
    usuario_logado=Depends(get_current_user)
):
    if not db.query(Aluno).filter(Aluno.id == aluno_id).first():
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    risco = calcular_risco_churn_completo(aluno_id, db, dados_csv)
    return {"aluno_id": aluno_id, "risco_churn_completo": risco}
