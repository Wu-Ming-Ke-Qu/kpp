import datetime

from django.db import models
from django.utils import timezone

from course.models import Course
from account.models import User
# Create your models here.
class Comment(models.Model):
    '''评论表'''

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.TextField(verbose_name="内容")
    zan = models.IntegerField(verbose_name="赞")
    cai = models.IntegerField(verbose_name="踩")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def is_recent(self):
        return ((timezone.now() - datetime.timedelta(days=3)) <= self.c_time)
    is_recent.admin_order_field = 'c_time'
    is_recent.boolean = True
    is_recent.short_description = '是否为新评论？'

    def approve_count(self):
        return self.vote_set.filter(attr="A").count()
    approve_count.admin_order_field = "c_time"
    approve_count.short_description = "计算赞数"

    def disapprove_count(self):
        return self.vote_set.filter(attr="D").count()
    disapprove_count.admin_order_field = "c_time"
    disapprove_count.short_description = "计算踩数"

    def is_folded(self):
        approve_count = self.approve_count()
        disapprove_count = self.disapprove_count()
        total_count = approve_count + disapprove_count
        if ((total_count >= 20) and 
            (disapprove_count / total_count >= 0.7)) or \
           ((total_count < 20) and 
            (disapprove_count >= 14)):
            return True
        return False
    is_folded.admin_order_field = "c_time"
    is_folded.boolean = True
    is_folded.short_description = "是否折叠？"

    def __str__(self) -> str:
        return (self.content if len(self.content) <= 10 else self.content[:10])
    
    def show_content(self):
        return (self.content if len(self.content) <= 10 else self.content[:10])
    show_content.admin_order_field = "content"
    show_content.short_description = "评论概要"

    class Meta:
        ordering = ['-c_time']
        verbose_name = '评论表'
        verbose_name_plural = '评论表'