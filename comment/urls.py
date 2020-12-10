from django.urls import path

from . import views

app_name = 'comment'
urlpatterns = [
    path('addcomment/', views.addcomment, name='addcourse'),
    path('rmcomment/<int:comment_id>', views.rmcomment, name='changecourseinfo'),
]