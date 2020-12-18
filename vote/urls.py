from django.urls import path

from . import views

app_name = 'vote'
urlpatterns = [
    path('like/<int:comment_id>', views.like, name='like'),
    path('dislike/<int:comment_id>', views.dislike, name='dislike'),
    path('clear/<int:comment_id>', views.clear, name='clear')
]