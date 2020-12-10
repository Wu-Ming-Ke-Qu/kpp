from django.urls import path

from . import views

app_name = 'school'
urlpatterns = [
    path('<int:school_id>', views.schoolinfo, name='schoolinfo')
]