
from kombu.mixins import ConsumerMixin
from app.queue.config import get_connection, queue
from app.database import SessionLocal
from app.models.checkin import Checkin
from datetime import datetime

class CheckinWorker(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(queues=[queue], callbacks=[self.processar_checkin], accept=["json"])
        ]

    def processar_checkin(self, body, message):
        db = SessionLocal()
        try:
            checkin = Checkin(
                aluno_id=body["aluno_id"],
                data_hora=datetime.fromisoformat(body["data_hora"])
            )
            db.add(checkin)
            db.commit()
            print(f"✅ Check-in processado para aluno {checkin.aluno_id}")
        except Exception as e:
            print(f"❌ Erro ao processar check-in: {e}")
        finally:
            db.close()
            message.ack()

if __name__ == "__main__":
    with get_connection() as conn:
        worker = CheckinWorker(conn)
        print("🔄 Aguardando mensagens na fila...")
        worker.run()
