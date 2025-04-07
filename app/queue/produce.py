import pika
import json

def enviar_checkins_em_lote(checkins):
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="checkin")
    channel.basic_publish(exchange="", routing_key="checkin", body=json.dumps(checkins))
    print("📨 Check-ins enviados para a fila!")
    connection.close()

def enviar_relatorio():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="relatorio")
    mensagem = json.dumps({"tipo": "relatorio_diario"})
    channel.basic_publish(exchange="", routing_key="relatorio", body=mensagem)
    print("📨 Pedido de relatório enviado!")
    connection.close()

def enviar_atualizacao_churn():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="churn_update")
    mensagem = json.dumps({"tipo": "reprocessar_churn"})
    channel.basic_publish(exchange="", routing_key="churn_update", body=mensagem)
    print("📨 Pedido de reprocessamento de churn enviado!")
    connection.close()
