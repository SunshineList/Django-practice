from django.urls import path, include
from rest_framework.routers import DefaultRouter
from yzm.views import refresh_captcha, get_yzm
from account.rest import api
from account.rest.router import HybridRouter

# router = DefaultRouter()
# urlpatterns = [
#     path('login/', api.login, name='login'),
#     path('logout/', api.logout, name='logout')
# ]

functions_and_view_classes = (
    ('用户登录', path('login/', api.login, name='restv1-login')),
    ('用户退出登录', path('logout/', api.logout, name='restv1-logout')),
    # ('用户信息', path('info/', api.query_info, name='restv1-info')),
    # ('验证码刷新', path('refresh_captcha/', refresh_captcha, name='restv1-refresh_captcha')),
    ('验证码获取', path('yzm', get_yzm, name='restv1-yzm')),
)

router = HybridRouter()
for api_name, func in functions_and_view_classes:
    router.add_api_view(api_name, func)

urlpatterns = [
    path('', include(router.urls))
]
