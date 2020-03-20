from django.contrib.auth.models import AbstractUser
from django.db import models

USER_TYPES = (
    ('0', '管理员'),
    ('1', '普通用户')
)
GENDERS = {
    ('0', '未知'),
    ('1', '男'),
    ('2', '女')
}


# Create your models here.
class MyUser(AbstractUser):
    type = models.CharField(u'类型', choices=USER_TYPES, default='1', max_length=2)
    mobile = models.CharField(u'手机号码', max_length=15, null=True, blank=True)
    # avatar = models.ImageField(upload_to=uuid_file_path, verbose_name=u'头像', null=True, blank=True)
    gender = models.CharField(u'性别', choices=GENDERS, default='0', max_length=1)
    birthday = models.DateField(u'生日', null=True, blank=True)
    note = models.TextField(u'管理员备注（用户不会看到）', null=True, blank=True)
    ips = models.TextField(u'IP历史', null=True, blank=True)

    class Meta:
        verbose_name = '账号'
        verbose_name_plural = '账号'

    def __unicode__(self):
        if self.first_name:
            return self.first_name
        return str(self.id)
