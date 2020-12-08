from django.contrib import admin
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    ordering = ('-c_time',)
    list_display = ('username', 'password', 
                    'email', 'school', 'department', 'is_active',
                    'total_approve', 'total_disapprove',
                    'is_new_user', 'c_time',)
    list_filter = ['school', 'department']
    search_fields = ['username']

@admin.register(models.EmailVerify)
class EmailVerifyAdmin(admin.ModelAdmin):
    ordering = ('-c_time',)
    list_display = ('code', 'email', 
                    'send_type', 'is_valid', 'c_time', )
    list_filter = ['send_type']
    search_fields = ['email']