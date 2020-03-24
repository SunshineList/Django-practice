from django.urls import path, include
from rest_framework.routers import DefaultRouter
from yzm.views import refresh_captcha, get_yzm, send_code_email
from account.rest import api
from account.rest.router import HybridRouter

# router = DefaultRouter()
# urlpatterns = [
#     path('login/', api.login, name='login'),
#     path('logout/', api.logout, name='logout')
# ]

functions_and_view_classes = (
    ('用户-登录', path('login/', api.login, name='restv1-login')),
    ('用户-退出登录', path('logout/', api.logout, name='restv1-logout')),

    ('账号-注册', path('register/', api.register, name='restv1-register')),
    ('账号-修改密码', path('change_pwd/', api.change_pwd, name='restv1-change-pwd')),
    # ('验证码刷新', path('refresh_captcha/', refresh_captcha, name='restv1-refresh_captcha')),
    ('验证码-获取', path('yzm', get_yzm, name='restv1-yzm')),
    ('验证码-邮箱验证', path('email_yzm', send_code_email, name='restv1-email-yzm'))

)

router = HybridRouter()
for api_name, func in functions_and_view_classes:
    router.add_api_view(api_name, func)

urlpatterns = [
    path('', include(router.urls))
]
