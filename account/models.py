import datetime

from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.conf import settings

from school.models import Department, School


class User(models.Model):
    '''用户表'''

    username = models.CharField(max_length=128, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=256, verbose_name="密码")
    email = models.EmailField(unique=True, verbose_name="邮箱")
    school = models.ForeignKey(School, 
                               on_delete=models.CASCADE, 
                               verbose_name="学校")
    department = models.ForeignKey(Department, 
                                   on_delete=models.CASCADE, 
                                   null=True, 
                                   blank=True, 
                                   verbose_name="院系")
    is_active = models.BooleanField("是否已激活？", default=False)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def is_new_user(self):
        return ((timezone.now() - datetime.timedelta(days=30)) <= self.c_time)
    is_new_user.admin_order_field = 'c_time'
    is_new_user.boolean = True
    is_new_user.short_description = '是否为新用户？'

    def total_approve(self):
        return sum([comment.approve_count() for comment in self.comment_set.all()])
    total_approve.admin_order_field = 'c_time'
    total_approve.short_description = '总赞数'
    
    def total_disapprove(self):
        return sum([comment.disapprove_count() for comment in self.comment_set.all()])
    total_disapprove.admin_order_field = 'c_time'
    total_disapprove.short_description = '总踩数'

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


class EmailVerify(models.Model):
    code = models.CharField(max_length=30, verbose_name="激活码")
    email = models.EmailField("邮箱")
    send_type = models.CharField(max_length=1, choices=(('r', '邮箱激活'), ('f', '忘记密码')), verbose_name='发送类型')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="生成时间")

    def is_valid(self):
        return ((timezone.now() - datetime.timedelta(days=settings.CONFIRM_DAYS)) < self.c_time)
    is_valid.admin_order_field = 'c_time'
    is_valid.boolean = True
    is_valid.short_description = '是否有效？'

    def __str__(self):
        return self.code + "(" + self.email + ")"

    class Meta:
        ordering = ['-c_time']
        verbose_name = '邮箱验证表'
        verbose_name_plural = '邮箱验证表'
