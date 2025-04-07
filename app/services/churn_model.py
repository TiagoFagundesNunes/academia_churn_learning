import os
import joblib
import pandas as pd
from datetime import datetime, timezone
from app.database import SessionLocal
from app.models.checkin import Checkin
from app.models.contrato import Contrato

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODELO_PATH = os.path.join(BASE_DIR, "modelos")

modelo_basico = joblib.load(os.path.join(MODELO_PATH, "modelo_churn_basico.pkl"))
modelo_completo = joblib.load(os.path.join(MODELO_PATH, "modelo_churn_completo.pkl"))

def calcular_variaveis_basicas(aluno_id: int, db):
    checkins = db.query(Checkin).filter(Checkin.aluno_id == aluno_id).order_by(Checkin.data_hora).all()
    if not checkins:
        return None

    total = len(checkins)
    data_primeiro = checkins[0].data_hora
    data_ultimo = checkins[-1].data_hora
    dias_ativos = (data_ultimo - data_primeiro).days or 1
    freq_semanal = (total / dias_ativos) * 7
    dias_sem_checkin = (datetime.utcnow() - data_ultimo).days
    duracoes = [c.duracao for c in checkins if c.duracao]
    duracao_media = sum(duracoes) / len(duracoes) if duracoes else 0

    contrato = db.query(Contrato).filter(Contrato.aluno_id == aluno_id, Contrato.ativo == True).first()
    tipo_plano = contrato.plano.tipo if contrato else "Desconhecido"

    return {
        "frequencia_semanal": round(freq_semanal, 2),
        "dias_desde_ultimo_checkin": dias_sem_checkin,
        "duracao_media_visitas": round(duracao_media, 2),
        "tipo_plano": tipo_plano
    }

def calcular_risco_churn(aluno_id: int, db):
    dados = calcular_variaveis_basicas(aluno_id, db)
    if not dados:
        return 0.9

    from sklearn.preprocessing import LabelEncoder
    tipo_plano_encoded = LabelEncoder().fit(["Silver", "Gold", "Premium", "Desconhecido"]).transform([dados["tipo_plano"]])[0]

    X = [[
        dados["frequencia_semanal"],
        dados["dias_desde_ultimo_checkin"],
        dados["duracao_media_visitas"],
        tipo_plano_encoded
    ]]
    probas = modelo_basico.predict_proba(X)[0]
    risco = probas[1] if len(probas) > 1 else probas[0]
    return round(risco, 2)

def calcular_risco_churn_completo(aluno_id: int, db, df_csv):
    dados = calcular_variaveis_basicas(aluno_id, db)
    if not dados:
        return 0.9

    row = df_csv[df_csv["aluno_id"] == aluno_id]
    if row.empty:
        return 0.9

    row = row.squeeze()
    from sklearn.preprocessing import LabelEncoder
    tipo_plano_encoded = LabelEncoder().fit(["Silver", "Gold", "Premium", "Desconhecido"]).transform([dados["tipo_plano"]])[0]
    genero_encoded = LabelEncoder().fit(["M", "F"]).transform([row["genero"]])[0]

    X = [[
        dados["frequencia_semanal"],
        dados["dias_desde_ultimo_checkin"],
        dados["duracao_media_visitas"],
        tipo_plano_encoded,
        row["frequencia_mensal"],
        row["dias_restantes"],
        row["duracao_plano"],
        int(row["frequentador_constante"]),
        genero_encoded,
        row["idade"],
        row["dias_ativos"]
    ]]
    prob = modelo_completo.predict_proba(X)[0][1]
    return round(prob, 2)
