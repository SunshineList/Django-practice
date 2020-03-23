from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.rest import api
from account.rest.router import HybridRouter

# router = DefaultRouter()

# urlpatterns = [
#     path('login/', api.login, name='login'),
#     path('logout/', api.logout, name='logout')
# ]

functions_and_view_classes = (
    ('登录', path('login/', api.login, name='restv1-login')),
    ('退出登录', path('logout', api.logout, name='restv1-logout'))
)

router = HybridRouter()
for api_name, func in functions_and_view_classes:
    router.add_api_view(api_name, func)

urlpatterns = [
    path('', include(router.urls))
]
