from course.models import Course
from account.models import User
from django.db import models

# Create your models here.
class Comment(models.Model):
    '''评论'''

    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    zan = models.IntegerField()
    cai = models.IntegerField()
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.content
    
    class Meta:
        ordering = ['c_time']
        verbose_name = '评论'
        verbose_name_plural = '评论'