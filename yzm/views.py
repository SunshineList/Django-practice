import json
from rest_framework.response import Response
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import JsonResponse, HttpResponse
# Create your views here.
# 创建验证码
from django.views import View


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
