# Academia - Sistema de Previsão de Churn com IA

Este projeto é uma API completa para gerenciamento de alunos de uma academia, com foco em **prever desistências (churn)** utilizando **modelos de Machine Learning**. Ele também implementa **filas assíncronas com RabbitMQ**, geração de **relatórios automáticos** e **dois modelos de IA**: um básico (para avaliação técnica) e um completo (com mais variáveis).

---

## Funcionalidades

-  Registro de alunos, planos e check-ins
-  Previsão de risco de churn com base no comportamento do aluno
-  Processamento assíncrono com RabbitMQ
-  Geração de relatórios diários via fila
-  Dois modelos preditivos de churn (básico e completo)
-  Interface interativa via Swagger

---

##  Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI** + Uvicorn
- **SQLAlchemy** + PostgreSQL
- **Scikit-learn** + Pandas (IA)
- **RabbitMQ**
- **Jupyter Notebook**

---

##  Instalação e Execução

### 1. Clone o repositório
git clone https://github.com/seu-usuario/academia-churn.git
cd academia-churn
2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
3. Instale as dependências
pip install -r requirements.txt
4. Configure o banco de dados PostgreSQL
Crie um banco chamado academia

Atualize a variável DATABASE_URL no arquivo app/database.py

5. Crie as tabelas no banco
python -m app.create_tables
6. Popule os dados iniciais
python -m app.seed_planos
python -m app.seed_contratos
python -m app.seed_checkins
7. Inicie a API
uvicorn app.main:app --reload
Acesse o Swagger: http://127.0.0.1:8000/docs

8. Execute os workers (em terminais separados)
python -m app.workers.checkin_worker
python -m app.workers.report_worker
python -m app.workers.churn_updater
 Dica: você pode automatizar isso com os arquivos .bat gerados na pasta starts/.

 Treinamento da IA
Execute o notebook para treinar os modelos de previsão:

jupyter notebook notebooks/modelo_churn.ipynb
📡 Produção de Mensagens (RabbitMQ)
No terminal interativo do Python:

python
from app.queue.produce import enviar_checkin, enviar_relatorio, enviar_atualizacao_churn
enviar_relatorio()
 Endpoints Principais
Método	Endpoint	Descrição
POST	/aluno/registro	Cadastra novo aluno
POST	/aluno/checkin	Registra check-in
POST	/aluno/checkout	Finaliza o check-in
GET	/aluno/{id}/frequencia	Lista o histórico de frequência
GET	/aluno/{id}/risco-churn	Previsão com modelo básico (atividade)
GET	/aluno/{id}/churn/completo	Previsão com modelo completo
 Limpar dados simulados
python -m app.limpar_dados_simulados
 Modelos de IA
🔹 Modelo Básico (atividade obrigatória):
Frequência semanal

Dias sem check-in

Duração média das visitas

Tipo de plano

 Modelo Completo (aprimorado):
Tudo do modelo básico, mais:

Idade

Gênero

Frequência mensal

Dias restantes no plano

Frequência constante

Dias ativos totais

 Status
✔ API funcional com Swagger
✔ Workers operando via RabbitMQ
✔ Modelos treináveis via Jupyter
✔ Sistema completo pronto para produção/testes