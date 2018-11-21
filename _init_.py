import logging
import ujson
from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from utils import OrderCodeMsg, OrderException

logger = logging.getLogger(__name__)


def responser(func):
    @wraps(func)
    #不改变使用装饰器原有函数的结构(如__name__, __doc__)
    def wrapper(*args, **kwargs):
        try:
            seria_class = args[0]
            req = args[1]
            use_ip = req.META.get('HTTP_USER_IP')
            logger.info("request from ip: {0}".format(use_ip))
            if seria_class.serializer_class:
            #第一次参数是可序列化的
                serialize = seria_class.get_serializer(data=req.data)
                if serialize.is_valid():
                    data = serialize.data
                    kwargs['data'] = data
                    result = func(*args, **kwargs)
                    resp = {
                        'code': result.code,
                        'code_msg': result.code_msg,
                        'message': result.message,
                        'data': result.data
                    }
                    return Response(data=resp, status=status.HTTP_200_OK)
                else:
                    resp = {
                        'code': OrderCodeMsg.PARAM_ERROR['code'],
                        'code_msg': OrderCodeMsg.PARAM_ERROR['msg'],
                        'message': '参数错误',
                        'data': serialize.errors
                    }
                    logger.error('response data: {0}'.format(resp))
                    return Response(data=resp,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                result = func(*args, **kwargs)
                resp = ujson.dumps(result)
                logger.info('response data: {0}'.format(resp))
                return Response(data=resp, status=status.HTTP_200_OK)
        except OrderException as e:
            msg = u'%s异常：%s' % (func.__name__, e)
            logger.error(msg, exc_info=True)
            resp = {
                'code': e.code,
                'code_msg': e.code_msg,
                'message': str(e)
            }
            return Response(data=resp,
                            status=status.HTTP_200_OK)
        except Exception as e:
            msg = 'response get except, msg: {0}'.format(e)
            logger.exception(msg, exc_info=True)
            data = '{"status": 0, "message": "unknow error ."}'
            return Response(data=data,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return wrapper
