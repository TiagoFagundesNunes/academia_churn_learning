
import os
import json
from kombu import Connection, Queue, Exchange, Consumer
from app.services.relatorios import gerar_relatorio_frequencia

rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672//")

def callback(body, message):
    print("📦 Mensagem recebida para gerar relatório diário!")
    try:
        if body.get("tipo") == "relatorio_diario":
            gerar_relatorio_frequencia()
            print("✅ Relatório gerado com sucesso.")
        else:
            print("⚠️ Tipo de mensagem desconhecido:", body)
    except Exception as e:
        print("❌ Erro ao processar relatório:", e)
    finally:
        message.ack()

def iniciar_worker():
    with Connection(rabbitmq_url) as conn:
        exchange = Exchange("default", type="direct")
        queue = Queue(name="relatorio", exchange=exchange, routing_key="relatorio")
        with Consumer(conn, queues=queue, callbacks=[callback], accept=["json"]):
            print("🔄 Aguardando pedidos de relatório...")
            while True:
                conn.drain_events()

if __name__ == "__main__":
    iniciar_worker()
