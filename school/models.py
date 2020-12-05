from django.db import models

# Create your models here.
class School(models.Model):
    '''学校'''

    school_name = models.CharField(max_length=128, unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.school_name
    
    class Meta:
        ordering = ['c_time']
        verbose_name = '学校'
        verbose_name_plural = '学校'

class Department(models.Model):
    '''院系'''

    department_name = models.CharField(max_length=128)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name
    
    class Meta:
        ordering = ['c_time']
        verbose_name = '院系'
        verbose_name_plural = '院系'

class Teacher(models.Model):
    '''教师'''

    teacher_name = models.CharField(max_length=128)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.teacher_name

    class Meta:
        ordering = ['c_time']
        verbose_name = '教师'
        verbose_name_plural = '教师'