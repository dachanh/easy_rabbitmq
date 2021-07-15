import time
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from kombu import Connection, Producer, Consumer, Queue, uuid

app = Flask(__name__)
api = Api(app)


class ProducerWorker(object):
    def __init__(self,url) -> None:
        super().__init__()
        self.connection = Connection(url)
        self.callback = Queue(uuid(), exclusive=True, auto_delete=True)
    def on_response(self,message):
        if message.properties['correlation_id'] == self.correlation_id:
            self.response = message.payload['result'] 
    def __call__(self,a,b,routing_key,exchange):
        self.response= None 
        self.correlation_id = uuid()
        with Producer(self.connection) as producer:
            producer.publish(
                {'a':a,'b':b},
                exchange=exchange,
                routing_key=routing_key,
                declare=[self.callback],
                reply_to = self.callback.name,
                correlation_id=self.correlation_id
            )
            with Consumer(self.connection,on_message=self.on_response,queues=[self.callback],no_ack=True):
                while self.response is None:
                    self.connection.drain_events()
        return self.response


     
url = 'amqp://guest:guest@localhost:5672//'
worker = ProducerWorker(url)

class testApi(Resource):
    def post(self):
        global worker
        res ={
            'div':None,
            'sum':None
        }
        routing_key = str(request.args.get('routing-key'))
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        res['sum'] = worker(a,b,routing_key=routing_key,exchange='task_add')
        res['div'] = worker(a,b,routing_key=routing_key,exchange='task_div')
        res = jsonify(res)
        res.status_code = 200
        return res
api.add_resource(testApi,'/')

if __name__ == "__main__":
    app.run('0.0.0.0',port=8181)