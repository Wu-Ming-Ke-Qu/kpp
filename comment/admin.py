from django.contrib import admin

from . import models
# Register your models here.

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    ordering=("-c_time",)
    list_display = ('show_content', 'course', 'user', 
                    'zan', 'cai', 'approve_count',
                    'disapprove_count', 'is_folded', 'c_time',)
    list_filter = ['course', 'c_time']
    search_fields = ['course__course_name', 'user__username', 'content']
