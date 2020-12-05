from django.db import models
from school.models import School, Department,Teacher
# Create your models here.
class Course(models.Model):
    '''课程'''

    course_name = models.CharField(max_length=128)
    course_id = models.CharField(max_length=128, unique=True, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    credit = models.IntegerField()
    hour = models.IntegerField()
    pre_course = models.CharField(max_length=128, null=True, blank=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name
    
    class Meta:
        ordering = ['c_time']
        verbose_name = '课程'
        verbose_name_plural = '课程'