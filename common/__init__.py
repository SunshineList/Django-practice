import logging

LOG = logging.getLogger('my.server')
BIZ = logging.getLogger('my.biz')
MNY = logging.getLogger('my.trade')


def is_assistant_app(request):
    return 'yherios' in request.META.get('HTTP_USER_AGENT', '').lower()
