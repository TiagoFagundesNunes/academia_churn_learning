from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# 🔐 Configurações do JWT
SECRET_KEY = "secretao123"
ALGORITHM = "HS256"
ACESSO_EXPIRA_MINUTOS = 60

# 🔒 Criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 Configura o esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/aluno/login")

# 🔐 Função para gerar hash da senha
def gerar_hash(senha: str) -> str:
    return pwd_context.hash(senha)

# 🔐 Verifica se a senha corresponde ao hash
def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)

# 🔐 Cria o token JWT com dados e tempo de expiração
def criar_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACESSO_EXPIRA_MINUTOS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔐 Extrai o ID do aluno do token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
