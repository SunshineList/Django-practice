from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from yzm.views import jarge_captcha, send_code_email
from yzm.models import EmailVerifyRecord
from account.rest.serializers import UserSerializer
from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model
from rest_framework.exceptions import ParseError
from django.contrib.auth.hashers import make_password, check_password
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
    """
    ##用户登录（普通用户）
    ---
    **参数说明**

    * username = admin
    * password = 1234qwer
    * yzm = IGHK


    **返回值**
    """
    pwd = request.data.get('password')
    LOG.debug("pwd %s", pwd)
    username = request.data.get('username')
    LOG.debug("username %s", username)
    yzm = request.POST.get("yzm")  # 用户提交的验证码
    key = request.POST.get("hash")  # 验证码答案
    # if not yzm or not key or not jarge_captcha(yzm, key):
    #     raise ParseError('验证码错误')
    user = authenticate(username=username, password=pwd)
    if user is None:
        user = authenticate(username=username, password=pwd)
        if user is None:
            raise ParseError('账号或者密码错误')
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    LOG.debug('ip  %s', ip)
    return Response(_login_user(request, user))

    # return Response({'msg': '登录成功'})


# 注销登录
@api_view(['GET'])
@permission_classes((UserAuth,))
def logout(request):
    """
    ##用户登出
    ---
    **参数说明**
    """
    user = request.user
    user.session_key = None
    user.save()
    django_logout(request)
    LOG.debug(user.session_key)
    return Response({'message': '您已安全退出'})


# 查询账号信息
@api_view(['POST'])
@permission_classes((UserAuth,))
def change_pwd(request):
    """
        ##修改密码
        **参数说明**

    * old_password
    * password：新密码
    * password2：重复新密码

    **返回值**

    * {'message': u'新密码已经生效，请重新登录'}
    """
    # user = request.user
    user = authenticate(username=request.user.username, password=request.data.get('old_password'))
    if user is None:
        raise ParseError('旧密码错误')

    password = request.data.get('password')
    if not password:
        raise ParseError('请输入新密码')

    if password != request.data.get('password2'):
        raise ParseError('两次输入的密码不一致')

    try:
        user.set_password(password)
    except Exception as e:
        LOG.exception(e)
        raise ParseError('请用字母与数字作为密码，不要包含其它字符')
    else:
        user.save()

    return Response({'message': '新密码设置成功，请登录'})


@api_view(['POST'])
def register(request):
    """
    ##用户注册
    ---

    **参数说明**

    * username
    * password
    * password2
    * email
    * email_key = alskmlkgasgnlsa
    **返回值**
    * 注册成功
    """
    username = request.data.get('username')
    if not username:
        raise ParseError('请输入用户名')
    password = request.data.get('password')
    if not password:
        raise ParseError('请输入新密码')
    if password != request.data.get('password2'):
        raise ParseError('两次输入的密码不一致')
    email = request.data.get('email')
    email_key = request.POST.get('email_key')
    LOG.debug("send_type  %s", email_key)
    if not email:
        raise ParseError('请确保邮箱和类型是否正确')
    is_success = EmailVerifyRecord.objects.filter(user=username, code=email_key).first()
    if not is_success:
        raise ParseError('邮箱验证码校验失败')
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        raise ParseError('该用户已被注册了，请直接登录')
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    with transaction.atomic():
        u = User.objects.create(username=username, password=make_password(password, None, 'pbkdf2_sha256'), type='1',
                                first_name=username, email=email,
                                ips=ip)
    if not u:
        raise ParseError('用户注册失败')
    return Response('注册成功')


# 查询账号信息
@api_view(['GET'])
# @permission_classes((UserAuth,))
def get_user_info(request):
    """
        ##用户信息
        ---
        **参数说明**
        **返回值**
        * {
            id:1,
            'username':admin
            'date_join':2020-03-29
            ...
        }
        """
    return Response(_login_user(request, request.user))
