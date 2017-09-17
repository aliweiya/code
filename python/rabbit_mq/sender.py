import pika

#establish a connection.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# create a channel
channel = connection.channel()

# create a queue named hello.
channel.queue_declare(queue='hello')

# producer can only publish to exchange, not to the queue.
channel.basic_publish(exchange='',
    routing_key='hello',
    body='hello world!')

connection.close()