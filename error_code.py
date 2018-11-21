# coding: utf-8


class OrderCodeMsg(object):
    """
    订单错误类型 code
    """
    SUCCESS = {'code': '0000', 'msg': 'success'}
    SUCCESS_CODE = SUCCESS['code']
    SUCCESS_MSG = SUCCESS['msg']

    PARAM_ERROR = {'code': '20001', 'msg': '参数错误'}
    PARAM_ERROR_CODE = PARAM_ERROR['code']
    SITE_ERROR = {'code': '20002', 'msg': '节点维护中'}
    TASK_ERROR = {'code': '20003', 'msg': '任务失败'}
    SOLD_OUT = {'code': '20004', 'msg': '节点售罄'}

    DATA_ERROR = {'code': '20101', 'msg': '数据异常'}
    DATA_ERROR_CODE = DATA_ERROR['code']
    DATA_PRO_ERROR = {'code': '20102', 'msg': '产品数据异常'}
    DATA_GOODS_ERROR = {'code': '20103', 'msg': '商品数据异常'}
    DATA_DUPLICATE_ERROR = {'code': '20104', 'msg': '数据重复'}

    ORDER_LOCK_ERROR = {'code': '20201', 'msg': '订单冲突'}
    ORDER_LOCK_ERROR_CODE = ORDER_LOCK_ERROR['code']
    ORDER_CAL_ERROR = {'code': '20202', 'msg': '订单算价异常'}
    ORDER_EXPIRE_ERROR = {'code': '20203', 'msg': '订单过期'}
    ORDER_BILL_ERROR = {'code': '20203', 'msg': '订单计费异常'}
    ORDER_CANCEL_BILL_ERROR = {'code': '20204', 'msg': '订单取消计费异常'}

    ACCOUNT_NO_BALANCE = {'code': '20301', 'msg': '账户余额不足'}
    ACCOUNT_NO_BALANCE_CODE = ACCOUNT_NO_BALANCE['code']
    ACCOUNT_BALANCE_ERROR = {'code': '20302', 'msg': '查询账户余额异常'}
    ACCOUNT_BALANCE_ERROR_CODE = ACCOUNT_BALANCE_ERROR['code']
    ACCOUNT_AUTH_ERROR = {'code': '20303', 'msg': '用户权限不足'}
    ACCOUNT_REVIEW_UNPASS = {'code': '20303', 'msg': '账户审核未通过'}
    
    OPERATE_ERROR = {'code': '20401', 'msg': u"操作异常"}
    OPERATE_ERROR_CODE = OPERATE_ERROR['code']

    UNKNOWN_ERROR = {'code': '9999', 'msg': '未知异常'}
    UNKNOWN_ERROR_CODE = UNKNOWN_ERROR['code']

    def __init__(self):
        pass


