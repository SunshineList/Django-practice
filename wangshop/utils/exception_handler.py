# -*- coding: utf-8 -*-
import sys

from rest_framework.response import Response
from rest_framework.views import exception_handler

from common import LOG


def my_exception_handler(exc, context):  # 200 will never be here
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:  # force 500 to 200, for the same error msg format
        exc_info = sys.exc_info()
        LOG.exception(exc)
        return Response({'error_code': 500, 'error': u'服务器繁忙，请稍后再试'})

    # add the HTTP status code to the response & force 200
    return Response({'error_code': response.status_code, 'error': response.data.get('detail')})
