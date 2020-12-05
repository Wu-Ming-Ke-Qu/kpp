from django.contrib import admin

from . import models
from course.models import Course
# Register your models here.
@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    ordering = ('-c_time',)
    list_display = ('school_name', 'email_addr', 'c_time')
    list_filter = ('c_time',)
    search_fields = ['school_name']
    
@admin.register(models.Department)
class Department(admin.ModelAdmin):
    ordering = ('-c_time',)
    list_display = ('department_name', 'school', 'c_time')
    list_filter = ('c_time',)
    search_fields = ['school_name']

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    ordering = ('-c_time',)
    list_display = ('teacher_name', 'school', 'department', 'show_course', 'c_time')
    list_filter = ('department', 'c_time', )
    search_fields = ["teacher_name", "school", "department", "show_course"]
    def show_course(self, obj):
        return [bt.course_name for bt in obj.courses.all()]
    show_course.short_description = '所授课程'
    inline = [
        CourseInline
    ]