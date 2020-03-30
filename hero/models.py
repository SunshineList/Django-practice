from django.db import models

GENGDER = (
    ('0', '未知'),
    ('1', '汉子'),
    ('2', '妹子')
)


# Create your models here.
class HeroModel(models.Model):
    hero = models.CharField('英雄', max_length=30, null=True, blank=True, unique=True)
    gender = models.CharField('性别', choices=GENGDER, default='1', null=True, blank=True, max_length=1)
    address = models.CharField('籍贯', max_length=50, null=True, blank=True)
    weizhi = models.CharField('位置', max_length=30, null=True, blank=True)
    taici = models.TextField('台词', null=True, blank=True)

    class Meta:
        verbose_name = '英雄'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = self.hero
        return name if name else self.id
