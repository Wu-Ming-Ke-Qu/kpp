from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('', views.userinfo, name='index'),
    path('certisuccess/', views.certi_success, name='certi_success'),
    path('emailcert/', views.email_cert, name='email_cert'),
    path('sendemailagain/', views.send_email_again, name="send_email_again"),
    path('changepw/', views.change_passwd, name="change_passwd")
]