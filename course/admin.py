from django.contrib import admin

from . import models

class TeacherInline(admin.TabularInline):
    model = models.CourseTeacher
    extra = 1

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_id', 
                    'school', 'department', 'show_teacher', 'credit',
                    'hour', 'pre_course', 'comment_count', 'c_time')
    list_filter = ('school', 'department', 'credit', )
    search_fields = ['course_name', 'course_id']
    def show_teacher(self, obj):
        return [bt.teacher_name for bt in obj.teachers.all()]
    show_teacher.short_description = '主讲教师'
    inlines=[
        TeacherInline
    ]

@admin.register(models.CourseTeacher)
class CourseTeacherAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'c_time')
    search_fields = ['course', 'teacher']