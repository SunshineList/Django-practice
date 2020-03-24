import datetime
from django.db import models
from django.conf import settings


# 邮箱验证
class EmailVerifyRecord(models.Model):
    # 验证码
    user = models.CharField('注册用户', max_length=30, null=True, blank=True)
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.CharField(max_length=50, verbose_name="邮箱", null=True, blank=True)
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10,
                                 choices=(("register", "注册"), ("retrieve", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", auto_now_add=True)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)
