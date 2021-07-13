import pika

def on_open(connection):
    connection.channel(on_open_callback=on_open_channel)

def on_open_channel(channel):
    channel.basic_publish(
        'exchange_name',
        'routing_key',
        pika.BasicProperties(content='text/plain',type='example')
    )

connection = pika.SelectConnection(on_open_callback=on_open)

try:
    connection.ioloop.start()
except:
    connection.close()
    connection.ioloop.start()