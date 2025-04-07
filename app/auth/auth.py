from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.aluno import Aluno

# Configuração JWT
SECRET_KEY = "segredo-super-seguro"  # troque isso em produção
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/aluno/login")

# Gera hash da senha
def gerar_hash(senha: str) -> str:
    return pwd_context.hash(senha)

# Verifica se a senha corresponde ao hash
def verificar_senha(senha: str, hash: str) -> bool:
    return pwd_context.verify(senha, hash)

# Gera o token JWT
def criar_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Obtém o usuário autenticado a partir do token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(lambda: SessionLocal())):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        aluno_id: str = payload.get("sub")
        if aluno_id is None:
            raise cred_exception
    except JWTError:
        raise cred_exception

    aluno = db.query(Aluno).filter(Aluno.id == int(aluno_id)).first()
    if aluno is None:
        raise cred_exception
    return aluno
