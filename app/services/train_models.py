import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Lê o CSV consolidado
df = pd.read_csv("data/dados_churn.csv")

# Encoding do plano (básico usa tipo_plano)
df["tipo_plano_encoded"] = LabelEncoder().fit_transform(df["tipo_plano"])

# ===== Modelo 1: Básico =====
X_basico = df[["frequencia_semanal", "dias_desde_ultimo_checkin", "duracao_media_visitas", "tipo_plano_encoded"]]
y = df["churn"]

modelo_basico = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_basico.fit(X_basico, y)
joblib.dump(modelo_basico, "data/modelo_churn_basico.pkl")

# ===== Modelo 2: Completo =====
# Codifica variáveis extras se necessário
df["genero_encoded"] = LabelEncoder().fit_transform(df["genero"])
df["frequentador_constante"] = df["frequentador_constante"].astype(int)

X_completo = df[[
    "frequencia_semanal", "dias_desde_ultimo_checkin", "duracao_media_visitas", "tipo_plano_encoded",
    "frequencia_mensal", "dias_restantes", "duracao_plano", "frequentador_constante",
    "genero_encoded", "idade", "dias_ativos"
]]

modelo_completo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_completo.fit(X_completo, y)
joblib.dump(modelo_completo, "data/modelo_churn_completo.pkl")

print("✅ Modelos treinados e salvos!")
