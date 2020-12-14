from django.db import models

# Create your models here.
class School(models.Model):
    '''学校表'''

    school_name = models.CharField(max_length=128, unique=True, verbose_name="学校")
    email_addr = models.CharField(max_length=254, unique=True, verbose_name="邮箱后缀")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.school_name
    
    class Meta:
        ordering = ['-c_time']
        verbose_name = '学校表'
        verbose_name_plural = '学校表'

class Department(models.Model):
    '''院系表'''

    department_name = models.CharField(max_length=128, verbose_name="院系名")
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="学校")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.department_name
    
    class Meta:
        ordering = ['-c_time']
        verbose_name = '院系表'
        verbose_name_plural = '院系表'

class Teacher(models.Model):
    '''教师表'''

    teacher_name = models.CharField(max_length=128, verbose_name="教师名")
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="学校", null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="院系", null=True, blank=True)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.teacher_name

    class Meta:
        ordering = ['-c_time']
        verbose_name = '教师表'
        verbose_name_plural = '教师表'