from django.urls import path
from rest_framework.routers import DefaultRouter
from account.rest import api

router = DefaultRouter()

urlpatterns = [
    path('login/', api.login, name='login'),
    path('logout/', api.logout, name='logout')
]
