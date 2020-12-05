from django.contrib import admin
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    ordering = ('-c_time',)
    list_display = ('username', 'password', 
                    'email', 'school', 'department', 
                    'total_approve', 'total_disapprove',
                    'is_new_user', 'c_time',)
    list_filter = ['school', 'department']
    search_fields = ['username']
