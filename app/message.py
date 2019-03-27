# encoding: utf-8
from collections import OrderedDict


def fail_msg(msg):
    message = {
        "status": 0,
        "message": msg
    }
    return message


def success_msg(msg='成功！', total_page='', **data):
    message = OrderedDict()
    if data: message['data'] = data
    message['status'] = 1
    message['message'] = msg
    if total_page: message['total_page'] = total_page
    return message
