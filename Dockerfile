# Usa imagem Python oficial
FROM python:3.11-slim

# Define diretório de trabalho no container
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do projeto
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
