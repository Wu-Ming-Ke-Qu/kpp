import datetime

from django.db import models
from django.utils import timezone
from django.db.models import Sum

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
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def is_new_user(self):
        return ((timezone.now() - datetime.timedelta(days=30)) <= self.c_time)
    is_new_user.admin_order_field = 'c_time'
    is_new_user.boolean = True
    is_new_user.short_description = '是否为新用户？'

    def total_approve(self):
        return self.comment_set.aggregate(Sum('zan'))['zan__sum']
    total_approve.admin_order_field = 'c_time'
    total_approve.short_description = '总赞数'
    
    def total_disapprove(self):
        return self.comment_set.aggregate(Sum('cai'))['cai__sum']
    total_disapprove.admin_order_field = 'c_time'
    total_disapprove.short_description = '总踩数'

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户表'
        verbose_name_plural = '用户表'