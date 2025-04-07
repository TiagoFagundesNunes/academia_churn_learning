import os
import pandas as pd
from datetime import datetime, date
from app.database import SessionLocal
from app.models.checkin import Checkin

def gerar_relatorio_frequencia():
    db = SessionLocal()
    hoje = date.today()

    checkins = db.query(Checkin).filter(
        Checkin.data_hora >= datetime.combine(hoje, datetime.min.time()),
        Checkin.data_hora <= datetime.combine(hoje, datetime.max.time())
    ).all()

    dados = [{
        "aluno_id": c.aluno_id,
        "entrada": c.data_hora,
        "saida": c.data_saida,
        "duracao_minutos": c.duracao
    } for c in checkins]

    df = pd.DataFrame(dados)
    os.makedirs("data/relatorios", exist_ok=True)
    caminho = f"data/relatorios/frequencia_{hoje}.csv"
    df.to_csv(caminho, index=False)

    db.close()
