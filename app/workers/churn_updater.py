
import os
import json
import subprocess
from kombu import Connection, Queue, Exchange, Consumer

rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672//")

def callback(body, message):
    print("📦 Mensagem recebida para atualizar o churn!")
    try:
        if body.get("tipo") == "reprocessar_churn":
            print("🔁 Reprocessando churn...")
            subprocess.run(["python", "analisar_dados.py"], check=True)
            subprocess.run(["python", "treinar_modelos.py"], check=True)
            print("✅ Modelos de churn atualizados com sucesso!")
        else:
            print("⚠️ Tipo de mensagem desconhecido:", body)
    except Exception as e:
        print("❌ Erro ao processar atualização de churn:", e)
    finally:
        message.ack()

def iniciar_worker():
    with Connection(rabbitmq_url) as conn:
        exchange = Exchange("default", type="direct")
        queue = Queue(name="churn_update", exchange=exchange, routing_key="churn_update")
        with Consumer(conn, queues=queue, callbacks=[callback], accept=["json"]):
            print("🔄 Aguardando pedidos de atualização do churn...")
            while True:
                conn.drain_events()

if __name__ == "__main__":
    iniciar_worker()
