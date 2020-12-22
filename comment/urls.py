from django.urls import path

from . import views

app_name = 'comment'
urlpatterns = [
    path('addcomment/<int:course_id>', views.addcomment, name='addcomment'),
    path('rmcomment/<int:comment_id>', views.rmcomment, name='rmcomment'),
]