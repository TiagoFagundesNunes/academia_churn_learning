import json
import os
from kombu import Connection, Exchange, Queue, Producer

rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")

def enviar_checkins_em_lote(checkins):
    with Connection(rabbitmq_url) as conn:
        channel = conn.channel()
        exchange = Exchange("default", type="direct")
        queue = Queue(name="checkin", exchange=exchange, routing_key="checkin")
        queue.maybe_bind(conn)
        queue.declare()

        producer = Producer(channel, exchange=exchange, routing_key="checkin")
        producer.publish(checkins, serializer="json")
        print("📨 Check-ins enviados para a fila!")

def enviar_relatorio():
    with Connection(rabbitmq_url) as conn:
        channel = conn.channel()
        exchange = Exchange("default", type="direct")
        queue = Queue(name="relatorio", exchange=exchange, routing_key="relatorio")
        queue.maybe_bind(conn)
        queue.declare()

        producer = Producer(channel, exchange=exchange, routing_key="relatorio")
        producer.publish({"tipo": "relatorio_diario"}, serializer="json")
        print("📨 Pedido de relatório enviado!")

def enviar_atualizacao_churn():
    with Connection(rabbitmq_url) as conn:
        channel = conn.channel()
        exchange = Exchange("default", type="direct")
        queue = Queue(name="churn_update", exchange=exchange, routing_key="churn_update")
        queue.maybe_bind(conn)
        queue.declare()

        producer = Producer(channel, exchange=exchange, routing_key="churn_update")
        producer.publish({"tipo": "reprocessar_churn"}, serializer="json")
        print("📨 Pedido de reprocessamento de churn enviado!")
