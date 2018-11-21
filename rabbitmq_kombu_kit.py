# -*- coding: utf-8 -*-
import logging
import traceback
from functools import wraps

from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from kombu.pools import producers

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def singleton(cls):
    instances = {}
    
    @wraps(cls)
    def _singleton(*args, **kargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kargs)
        return instances[cls]
    
    return _singleton


class TaskConnection(Connection):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TaskConnection, cls).__new__(cls, *args,
                                                               **kwargs)
        return cls._instance


class Publisher(object):
    def __init__(self, amqp_url, exchange=None, exchange_type=None,
                 routing_key=None):
        logger.info(
            '建立RMQ连接开始,url: %s, exchange: %s, exchange_type: %s, routing_key: %s',
            amqp_url,
            exchange,
            exchange_type,
            routing_key)
        self.amqp_url = amqp_url
        self.exchange = Exchange(exchange,
                                 type=exchange_type if exchange_type else 'direct')
        self.routing_key = routing_key
        self._connection = None
        self._message_number = 0
        self._connection = TaskConnection(amqp_url, heartbeat=1)
        logger.info('建立RMQ连接结束')
    
    def publish_message(self, payload, expiration=None):
        logger.info(self._connection)
        try:
            self._connection.heartbeat_check()
            with producers[self._connection].acquire(block=True,
                                                     timeout=3) as producer:
                logger.info(producer)
                producer.publish(payload,
                                 exchange=self.exchange,
                                 declare=[self.exchange],
                                 routing_key=self.routing_key,
                                 app_id='publisher',
                                 expiration=expiration,
                                 retry=True,
                                 retry_policy={'max_retries': 3})
                self._message_number += 1
                self._connection.release()
                logger.info('Published message # %i: %s', self._message_number,
                            payload)
        except Exception as exc:
            logger.error('发送消息 %s 失败, raise Exception: %r', payload, exc,
                         exc_info=True)
            raise exc
    
    def close(self):
        self._connection.release()


class Consumer(ConsumerMixin):
    
    def __init__(self, amqp_url, exchange=None, exchange_type=None, queues=[]):
        self.amqp_url = amqp_url
        self.connection = None
        self.connection = TaskConnection(amqp_url)
        self.exchange = self.declare_exchange(exchange, exchange_type)
        self.queues = [Queue(q.get('queue'), self.exchange,
                             routing_key=q.get('routing_key')) for q in queues]
    
    def get_consumers(self, ClassConsumer, channel):
        cs = [ClassConsumer(queues=self.queues, callbacks=[self.on_message])]
        for c in cs:
            c.qos(prefetch_count=1)
        return cs
    
    def on_message(self, body, message):
        logger.info('Received Message # %s from %s: %s',
                    message.delivery_tag,
                    message.properties.get('app_id', None), body)
        try:
            routing_key = message.delivery_info.get('routing_key')
            getattr(self, self.QUEUE_CALLBACK.get(routing_key))(body)
            message.ack()
            logger.info('Task done for message # %s\n', message.delivery_tag)
        except Exception as exc:
            logger.error(traceback.format_exc())
            logger.error('Process Message # %s raised exception: %r',
                         message.delivery_tag, exc)
            message.reject()
    
    def process_task(self, body):
        import time
        time.sleep(10)
        pass
    
    def declare_exchange(self, name='', type='', binding=None):
        channel = self.connection.channel()
        exchange = Exchange(name, type, channel)
        exchange.declare()
        if binding:
            bind_ex = Exchange(binding[0], binding[1], channel)
            bind_ex.bind_to(exchange, binding[2])
        channel.close()
        return exchange
    
    def declare_queue(self, name='', exchange='', routing_key='',
                      queue_arguments=None):
        channel = self.connection.channel()
        exchange = exchange or self.exchange
        queue = Queue(name, exchange, routing_key, channel)
        if queue_arguments:
            queue.queue_arguments = queue_arguments
        queue.declare()
        channel.close()
        return queue
    
    def close(self):
        self.connection.release()
        self.should_stop = True


def main_consumer():
    # logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    
    example = Consumer('amqp://guest:guest@localhost:5672/%2F',
                       exchange='task',
                       exchange_type='direct', queues=['task'])
    try:
        example.run()
    except KeyboardInterrupt:
        example.close()


def main_producer():
    # for x in range(0, 100):
    # Connect to localhost:5672 as guest with the password guest and virtual host "/" (%2F)
    example = Publisher('amqp://guest:guest@172.20.3.1:22022/%2F',
                        exchange='exchange_task',
                        exchange_type='direct', routing_key='queue_task')
    try:
        logger.info('Run Here....................')
        example.publish_message(
            {'task_id': 'fb58f8af-1740-11e6-8246-001e64e0e7b9'})
        logger.info('Run Finish .................\n')
    except KeyboardInterrupt:
        example.close()


if __name__ == '__main__':
    amqp_url = 'amqp://guest:guest@127.0.0.1:5672/%2F'
    import sys
    
    for x in range(0, 100):
        print(sys.argv, sys.argv[1])
        if sys.argv[1] == 'producer':
            main_producer()
        elif sys.argv[1] == 'consumer':
            main_consumer()
    # exchange = Exchange('exchange_task', type='direct')
    # dlx_exchange = Exchange('test_dlx123')
    # conn = TaskConnection(amqp_url)
    # channel = conn.channel()
    # bound_ex = dlx_exchange(channel)
    # bound_ex.bind_to('exchange_task', 'queue_subtask')
    # bound_ex.declare()
    # kwargs = {
    #     'x-dead-letter-exchange': 'test_dlx123',
    #     'x-dead-letter-routing-key': 'queue_subtask'
    # }
    # queue = Queue('test_delay_queue123', bound_ex, routing_key='test_delay')
    # queue.queue_arguments = kwargs
    # bound_queue = queue(channel)
    # bound_queue.declare()
    # print('12')
