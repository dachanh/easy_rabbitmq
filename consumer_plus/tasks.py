import time
import random
from logging import Logger
from kombu.utils.functional import reprcall
from kombu.log import get_logger
from kombu.mixins import ConsumerProducerMixin
from kombu import Exchange, Queue , Connection
from task_queue import taskQueue

Logger = get_logger(__name__)


class Worker(ConsumerProducerMixin):
    def __init__(self,connection) -> None:
        super().__init__()
        self.connection = connection



    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=taskQueue,
            accept={'application/json'},
            prefetch_count=1,
            on_message=self.process_task)]

    def process_task(self,message):
        a = message.payload['a']
        b = message.payload['b']
        time.sleep(random.randint(0,2))
        c ={'result':a+b}

        self.producer.publish(
            c,exchange='',routing_key=message.properties['reply_to'],
            correlation_id=message.properties['correlation_id'],
            serializer='json',
            retry=True
        )
        message.ack()


def start_worker(url):
    with Connection('amqp://guest:guest@localhost:5672//') as conn:
        try:
            worker = Worker(conn)
            worker.run()
        except KeyboardInterrupt:
            print('bye bye')
if __name__ == '__main__':
    try:
        start_worker('amqp://guest:guest@localhost:5672//')
    except KeyboardInterrupt:
        pass