from kombu import Connection, Exchange, Queue

RABBITMQ_URL = "amqp://guest:guest@localhost:5672//"

exchange = Exchange("checkin", type="direct")
queue = Queue(name="checkin_queue", exchange=exchange, routing_key="checkin")

def get_connection():
    return Connection(RABBITMQ_URL)
