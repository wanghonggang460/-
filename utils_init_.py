# coding: utf-8
import datetime
import functools
import logging
import random
import time
import uuid

from utils.error_code import OrderCodeMsg

logger = logging.getLogger(__name__)


def create_uuid(name=''):
    '''
    自动生成36位uuid
    :param name:
    :return:
    '''
    return str(uuid.uuid1())


def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        s = time.time()
        func(*args, **kw)
        e = time.time()
        logger.info('func: {0} >use_time: {1}s'.format(func.__name__, e - s))
    return wrapper


class Cache(object):
    ''' cache operate pack
    '''

    @classmethod
    def set(cls, key, value, timeout=None):
        try:
            pass
        except Exception as e:
            pass

    @classmethod
    def get(cls, key):
        try:
            pass
        except Exception as e:
            pass

    @classmethod
    def delete(cls, key):
        try:
            pass
        except Exception as e:
            pass

    @classmethod
    def ttl(cls, key):
        try:
            pass
        except Exception as e:
            pass


class OrderException(Exception):
    """
    订单异常
    """
    
    def __init__(self, order_code_msg, *args, **kwargs):
        self._code = order_code_msg.get('code', '9999')
        self._code_msg = order_code_msg.get('msg', '未知异常')
        self.order_code_msg = order_code_msg
        super(OrderException, self).__init__(*args, **kwargs)
    
    @property
    def code(self):
        return self._code
    
    @property
    def code_msg(self):
        return self._code_msg
    
    @property
    def msg(self):
        return '%s(%s):%s' % (self._code_msg, self.code, self.__str__())


class OrderReturn(object):
    """
    订单返回数据
    """

    def __init__(self, order_code_msg, message='', data=None):
        self.order_code_msg = order_code_msg
        self.message = message
        self.data = data if data is not None else {}
    
    @property
    def code(self):
        return self.order_code_msg['code']
    
    @property
    def code_msg(self):
        return self.order_code_msg['msg']
    
    def is_success(self):
        if self.code == OrderCodeMsg.SUCCESS_CODE:
            return True
        return False


def catch_order_exception(op_msg):
    def _wrapper(func):
        def deco(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except OrderException as e:
                msg = '%s异常：%s' % (op_msg, e)
                logger.error(msg, exc_info=True)
                return OrderReturn(e.order_code_msg, str(e))
            except Exception as ex:
                msg = '%s异常：%s' % (op_msg, ex)
                logger.error(msg, exc_info=True)
                return OrderReturn(OrderCodeMsg.UNKNOWN_ERROR, msg)
        
        return deco
    
    return _wrapper


def create_order_code():
    '''
    自动生成uuid
    :param name:
    :return:
    '''
    return datetime.datetime.now().strftime('%Y%m%d%H%S') + create_random_No(6)


def create_random_No(len_=6):
    '''
    生成随机数字
    :param len_:默认长度6
    :return:len_长度的随机数字
    '''
    num = ''
    for i in range(len_):
        num += str(random.randrange(10))
    logger.debug(num)
    return num
