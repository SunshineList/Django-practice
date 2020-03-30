from django.contrib import admin
from hero.models import HeroModel


# Register your models here.

@admin.register(HeroModel)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('hero', 'gender', 'address', 'weizhi', 'taici',)
    search_fields = ('hero',)
