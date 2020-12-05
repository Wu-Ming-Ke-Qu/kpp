from django.contrib import admin

from . import models
# Register your models here.

@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    ordering = ('-ch_time', )
    list_display = ('user', 'comment', 
                    'attr', 'is_recent_vote', 'ch_time')
    list_filter = ('user', 'comment', 'ch_time', )
    search_fields = ['user', 'comment']
