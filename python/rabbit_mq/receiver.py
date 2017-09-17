import pika

#establish a connection.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# create a channel
channel = connection.channel()

# create a queue named hello.
channel.queue_declare(queue='hello')

# fair dispatch
channel.basic_qos(prefetch_count=1)  

# define a callback function to process the data received
# %r using the repr() method to process object
# %s using the str() method to process object
def callback(ch, method, properties, body):
    print 'Received %r' % (body)

    # ack
    # ch.basic_ack(delivery_tag = method.delivery_tag) 

channel.basic_consume(callback,
    queue='hello',
    no_ack=True)

# endless loop listening
print 'waiting for messages'
channel.start_consuming()