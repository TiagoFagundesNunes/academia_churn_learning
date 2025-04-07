# analisar_dados.py

from app.database import SessionLocal
from app.models.checkin import Checkin
from app.models.contrato import Contrato
from app.models.plano import Plano
from datetime import datetime, timezone
import pandas as pd

# Conecta ao banco
db = SessionLocal()

# Carrega os check-ins do banco
checkins = db.query(Checkin).all()

# Agrupa check-ins por aluno
dados_por_aluno = {}
for c in checkins:
    aluno_id = c.aluno_id
    if aluno_id not in dados_por_aluno:
        dados_por_aluno[aluno_id] = {
            "checkins": [],
            "duracoes": []
        }
    dados_por_aluno[aluno_id]["checkins"].append(c.data_hora)
    if c.data_saida and c.duracao:
        dados_por_aluno[aluno_id]["duracoes"].append(c.duracao)

# Carrega dados adicionais do CSV
alunos_df = pd.read_csv("data/dados_alunos.csv")
alunos_df["data_nascimento"] = pd.to_datetime(alunos_df["data_nascimento"])
alunos_df["data_inicio"] = pd.to_datetime(alunos_df["data_inicio"])
alunos_df["idade"] = alunos_df["data_nascimento"].apply(
    lambda x: (datetime.now() - x).days // 365
)

linhas = []

for aluno_id, dados in dados_por_aluno.items():
    checkin_datas = sorted(dados["checkins"])
    duracoes = dados["duracoes"]

    if not checkin_datas:
        continue

    # Frequência semanal
    if len(checkin_datas) > 1:
        dias_total = (checkin_datas[-1] - checkin_datas[0]).days or 1
        semanas = dias_total / 7
        freq_semanal = round(len(checkin_datas) / semanas, 2)
    else:
        freq_semanal = 1.0

    # Dias desde o último check-in
    dias_desde_ultimo = (datetime.now(timezone.utc).replace(tzinfo=None) - checkin_datas[-1]).days

    # Duração média das visitas
    duracao_media = round(sum(duracoes) / len(duracoes), 2) if duracoes else 0

    # Dados do contrato
    contrato = db.query(Contrato).filter(
        Contrato.aluno_id == aluno_id, Contrato.ativo == True
    ).first()
    tipo_plano = "Desconhecido"
    duracao_plano = 1
    if contrato and contrato.plano:
        tipo_plano = contrato.plano.tipo
        duracao_plano = contrato.plano.duracao_plano

    # Dados do CSV
    aluno_info = alunos_df[alunos_df["id"] == aluno_id].squeeze()
    if aluno_info.empty:
        continue

    linha = {
        "aluno_id": aluno_id,
        "frequencia_semanal": freq_semanal,
        "dias_desde_ultimo_checkin": dias_desde_ultimo,
        "duracao_media_visitas": duracao_media,
        "tipo_plano": tipo_plano,
        "frequencia_mensal": aluno_info["frequencia_mensal"],
        "dias_restantes": aluno_info["dias_restantes"],
        "duracao_plano": duracao_plano,
        "frequentador_constante": aluno_info["frequentador_constante"],
        "genero": aluno_info["genero"],
        "idade": aluno_info["idade"],
        "dias_ativos": aluno_info["dias_ativos"],
        "churn": aluno_info["churn"],
    }

    linhas.append(linha)

# Salva no arquivo final de churn
df_final = pd.DataFrame(linhas)
df_final.to_csv("data/dados_churn.csv", index=False)
print("✅ Arquivo data/dados_churn.csv gerado com sucesso!")

db.close()
