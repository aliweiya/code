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


# exchange
channel.exchange_declare(exchange='logs', type='fanout')

channel.basic_publish(exchange='logs',
    routing_key='',
    body=message)


# queue without a name
result = channel.queue_declare()  
print result.method.name

# close the queue
result = channel.queue_declare(exclusive=True)

channel.queue_bind(exchange='logs', 
    queue=result.method.queue)


# routing
channel.exchange_declare(exchange='direct_logs',  
    type='direct')

# severity：'info', 'warning', 'error'.
channel.basic_publish(exchange='direct_logs',  
    routing_key=severity,  
    body=message) 

result = channel.queue_declare(exclusive=True)
queue_name = result.method.name

for severity in serverities:
    channel.queue_bind(exchange='direct_logs',
        queue=queue_name,
        routing_key=severity)


