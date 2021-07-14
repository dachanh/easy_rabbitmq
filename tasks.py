from celery import Celery
from kombu import Exchange, Queue
from celery.exceptions import Reject


defaultQueueName = 'default'
defaultExchangeName = 'default'
defaultRoutingName = 'default'


sunshineQueueName = 'moon'
sunshineRoutingKey = 'moon'

moonQueueName = 'moon'
moonRoutingKey = 'moon'

app = Celery('workerCelery',broker='amqp://guest@localhost:5672//',backend='redis://localhost:6379/0')


defaultExchange = Exchange(default_exchange=defaultExchangeName,type='direct')

defaultQueue = Queue(
    default_queue=defaultQueueName,
    default_exchange= defaultExchangeName,
    routing_key=defaultRoutingName
)

sunshineQueue = Queue(sunshineQueueName,defaultExchangeName,sunshineRoutingKey)
moonQueue = Queue(moonQueueName,defaultExchangeName,moonRoutingKey)

app.conf.task_queue = (defaultQueue,sunshineQueue,moonQueue)
app.conf.task_default_exchange = defaultExchange
app.conf.task_default_routing_key = defaultRoutingName


@app.task
def add(x,y):
    return x + y


