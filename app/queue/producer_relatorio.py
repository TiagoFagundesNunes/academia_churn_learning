import pika
import json

def solicitar_relatorio_diario():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="relatorio_diario")

    channel.basic_publish(
        exchange="",
        routing_key="relatorio_diario",
        body=json.dumps({"acao": "gerar"})
    )
    connection.close()
