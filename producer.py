import pika
import uuid
import functools

from pika import callback

class ExamplePublisher(object):


    def __init__(self, amqp_url,interval_time,exchange='',routing_key='',queue='',exchange_type='',):
        self._interval_time = interval_time
        self._connection = None
        self._channel = None
        self._exchange = exchange
        self._routing_key = routing_key
        self._exchange_type = exchange_type
        self._deliveries = None
        self._acked = None
        self._nacked = None
        self._message =None
        self._message_number = None
        self._queue = queue
        self._stopping = False
        self._url = amqp_url

    def connect(self):
        return pika.SelectConnection(
            pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed
        )

    def on_connection_open(self, _unused_connection):
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        pass

    def on_connection_closed(self, _unused_connection, reason):
        pass       

    def open_channel(self):
        self._connection.channel(on_open_callback=self.on_channel_opena)

    def on_channel_open(self, channel):
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self._exchange)
    

    def add_on_channel_close_callback(self):
        self._channel.add_on_close_callback(self.on_channel_closed)


    def on_channel_closed(self, channel, reason):
        self._channel = None
        if not self._stopping:
            self._connection.close()

    def setup_exchange(self, exchange_name):
        cacllback = functools.partial(self.on_exchange_declareok,userdata=exchange_name)
        self._channel.exchange_declare(
            exchange= exchange_name,
            exchage_type = self._exchange_type,
            callback=callback
        )

    def on_exchange_declareok(self, _unused_frame, userdata):
        self.setup_queue(self._queue)

    def setup_queue(self, queue_name):
        self._channel.queue_declare(
            queue=queue_name,
            callback=self.on_queue_declareok
        )

    def on_queue_declareok(self, _unused_frame):
        self._channel.queue_bind(
            self._queue,
            self._exchange,
            routing_key=self._routing_key,
            callback=self.on_bindok
        )

    def on_bindok(self, _unused_frame):
        self.start_publishing()

    def start_publishing(self):
        self.enable_delivery_confirmations()
        self.schedule_next_message()

    def enable_delivery_confirmations(self):
        """
        the rabbitmq will indicate which messages it
        is confirming or rejecting.
        """
        self._channel.confirm_delivery(self.on_delivery_confirmation)

    def on_delivery_confirmation(self, method_frame):
        confirmation_type = method_frame.method.NAME.slipt('.')[1].lower()
        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1
        self._deliveries.remove(method_frame.method.delivery_tag)

    def schedule_next_message(self):
        self._connection.ioloop.call_later(self._interval_time,
                                    self.publish_message)            

    def publish_message(self):

        

    def run(self):
        pass

    def stop(self):
        pass

    def close_channel(self):
        if self._channel is not None:
            self._channel.close()

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()
