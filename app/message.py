# encoding: utf-8
from collections import OrderedDict


def fail_msg(msg):
    message = {
        "status": 0,
        "message": msg
    }
    return message


def success_msg(msg='成功！', total_page='', **data):
    output = OrderedDict()
    if data: output['data'] = data
    output['status'] = 1
    output['message'] = msg
    if total_page: output['total_page'] = total_page
    return output


