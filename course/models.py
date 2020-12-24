from django.db import models
from django.db.models import Sum

from school.models import School, Department, Teacher
# Create your models here.
class Course(models.Model):
    '''课程表'''

    course_name = models.CharField(max_length=128, 
                                   verbose_name="课程名")
    course_id = models.CharField(max_length=128, unique=True, 
                                 null=True, blank=True, verbose_name="课程号")
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="学校")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="开课院系")
    teachers = models.ManyToManyField(Teacher, through='CourseTeacher', 
                                     through_fields=('course', 'teacher'), 
                                     verbose_name=u"开课教师", related_name='courses')
    credit = models.CharField(max_length=128, verbose_name="学分")
    hour = models.CharField(max_length=128, verbose_name="学时")
    pre_course = models.CharField(max_length=128, null=True, blank=True, verbose_name="先修要求")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def comment_count(self):
        return self.comment_set.count()
    comment_count.admin_order_field = 'c_time'
    comment_count.short_description = '评论总数'
    
    def total_approve(self):
        return self.comment_set.aggregate(Sum('zan'))['zan__sum']
    total_approve.admin_order_field = 'c_time'
    total_approve.short_description = '总赞数'

    def total_disapprove(self):
        return self.comment_set.aggregate(Sum('cai'))['cai__sum']
    total_disapprove.admin_order_field = 'c_time'
    total_disapprove.short_description = '总踩数'

    def __str__(self):
        return self.course_name
    
    class Meta:
        ordering = ['-c_time']
        verbose_name = '课程表'
        verbose_name_plural = '课程表'

class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="教师")
    c_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    def __str__(self):
        return str(self.course)
    
    class Meta:
        ordering = ['-c_time']
        verbose_name = '课程教师中间表'
        verbose_name_plural = '课程教师中间表'