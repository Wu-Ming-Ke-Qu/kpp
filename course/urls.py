from django.urls import path

from . import views

app_name = 'course'
urlpatterns = [
    path('addcourse/', views.addcourse, name='addcourse'),
    path('changecourseinfo/', views.changecourseinfo, name='changecourseinfo'),
    path('<int:course_id>', views.courseinfo, name='courseinfo')
]