import hashlib
import json
import uuid

from django.core.cache import cache
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from rest_framework.response import Response

from yzm.models import EmailVerifyRecord  # 邮箱验证model
from common import LOG
from django.conf import settings
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import JsonResponse, HttpResponse


# 创建验证码

def captcha():
    ret = {}
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    ret['hashkey'] = hashkey
    image_url = captcha_image_url(hashkey)  # 验证码地址
    ret['image_url'] = image_url
    # captcha = {'hashkey': hashkey, 'image_url': image_url}
    return JsonResponse(ret)


# 刷新验证码
def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


# 验证验证码
def jarge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            if get_captcha.response == captchaStr.lower():  # 如果验证码匹配
                return True
        except:
            return False
    else:
        return False


def get_yzm(request):
    """
       ##验证码获取##
       **参数说明**
       """
    ret = {}
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    ret['hashkey'] = hashkey
    image_url = captcha_image_url(hashkey)  # 验证码地址
    ret['image_url'] = image_url
    return JsonResponse(ret)


# 生成随机字符串
def random_str(randomlength=6):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


@transaction.atomic
@api_view(['POST'])
# 发送电子邮件
def send_code_email(request):
    """
    ##发送电子邮件
    * 参数说明
        username: 注册的用户名
        email: 要发送的邮箱
        send_type: 邮箱类型(register 注册 retrieve找回密码)
    返回值：发送失败/msg:发送成功
    """
    data = request.data
    user = data.get('username')
    if not user:
        raise ParseError('注册用户不能为空')
    LOG.debug("email  %s", data.get('email'))
    send_type = data.get('send_type')
    LOG.debug("send_type  %s", data.get('send_type'))
    email = data.get('email')
    if not send_type or not email:
        raise ParseError('邮箱和类型不能为空')
    code = random_str(6)
    email_record = EmailVerifyRecord.objects.create(user=user, code=code, email=email, send_type=send_type)
    if not email_record:
        raise ParseError('创建失败')
    email_record.save()
    # 如果为注册类型
    if send_type == "register":
        email_title = "注册激活"
        # email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
        if not send_status:
            raise ParseError('发送失败')
    if send_type == "retrieve":
        email_title = "找回密码"
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
        if not send_status:
            raise ParseError('发送失败')
    return Response({'msg': '发送成功'})
