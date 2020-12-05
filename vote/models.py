import datetime

from django.db import models
from django.utils import timezone

from account.models import User
from comment.models import Comment

# Create your models here.
class Vote(models.Model):
    '''投票表'''

    LIKES = (
        ('A', '赞'),
        ('D', '踩'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="评论")
    attr = models.CharField(max_length=1, verbose_name="赞踩情况", choices=LIKES)
    ch_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    def __str__(self):
        return self.get_attr_display()
    
    def is_recent_vote(self):
        now = timezone.now()
        return now - datetime.timedelta(days=3) <= self.ch_time
    is_recent_vote.admin_order_field = 'ch_time'
    is_recent_vote.boolean = True
    is_recent_vote.short_description = '是否最近？'

    class Meta:
        ordering = ['-ch_time']
        verbose_name = '投票表'
        verbose_name_plural = '投票表'