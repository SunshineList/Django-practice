from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from account.rest.serializers import UserSerializer
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework.exceptions import ParseError

from common import LOG


# 登录验证
def _login_user(request, user):
    if not user.is_active:
        raise ParseError(u'你的账户有异常，请联系客服%s' % '正午')
    django_login(request, user)
    limit = 5  # 如果没有session_key尝试写入5次
    while not request.session.session_key:
        LOG.warn('session is empty, try=%d', limit)
        for k, v in request.session.iteritems():
            LOG.warn('%s = %s', k, v)
        django_logout(request)
        django_login(request, user)
        if not request.session.get('has_session'):
            request.session['has_session'] = True
        limit -= 1
        if limit < 0:
            break
    user.session_key = request.session.session_key
    user.save()
    return UserSerializer(user).data


# 权限验证
class UserAuth(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if not request.user.is_active:
                raise PermissionDenied(u'该账号已停用，请联系管理员')
            if not request.user.is_staff:
                raise PermissionDenied(u'该账号登录状态有误，请联系管理员')
            return True
        raise PermissionDenied(u'请先登录')


@api_view(['POST'])
def login(request):
    '''
    ##用户登录（普通用户）
    ---
    **参数说明**

    * username=admin
    * password=1234qwer

    **返回值**
    '''
    pwd = request.data.get('password')
    LOG.debug("pwd %s", pwd)
    username = request.data.get('username')
    LOG.debug("username %s", username)
    user = authenticate(username=username, password=pwd)
    if user is None:
        user = authenticate(username=username, password=pwd)
        if user is None:
            raise ParseError(u'账号或者密码错误')
    data = Response(_login_user(request, user))
    return data


# 注销登录
@api_view(['GET'])
@permission_classes((UserAuth,))
def logout(request):
    '''
    ##用户登出
    ---
    **参数说明**
    '''
    user = request.user
    user.session_key = None
    user.save()
    django_logout(request)
    LOG.debug(user.session_key)
    return Response({'message': '您已安全退出'})
