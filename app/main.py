from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from app.routers import aluno, checkin, contrato, checkin_massa, relatorio

app = FastAPI(
    title="API Academia - Registro e IA de Previsão de Churn!",
    description="Sistema para registrar frequência e prever desistência de alunos.",
    version="1.0.0"
)

# CORS (caso use frontend depois)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas organizadas por entidade
app.include_router(aluno.router, prefix="/aluno", tags=["Aluno"])
app.include_router(checkin.router, prefix="/aluno", tags=["Check-in"])
app.include_router(contrato.router, prefix="/aluno", tags=["Contrato"])
app.include_router(checkin_massa.router, prefix="/aluno", tags=["Check-in em Massa"])
app.include_router(relatorio.router, tags=["Relatórios"])

@app.get("/")
def read_root():
    return {"mensagem": "API da Academia está ativa!"}

# Swagger com suporte a JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/aluno/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"OAuth2PasswordBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
