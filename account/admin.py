from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from account.models import MyUser


@admin.register(MyUser)
class UserAdmin(UserAdmin):
    list_display = ('type', 'username', 'email', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'type', 'birthday',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
