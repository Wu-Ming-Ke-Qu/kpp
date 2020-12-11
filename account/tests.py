import datetime
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .models import User
from .models import EmailVerify

# create an instance of the client for our use
client = Client()

# Create your tests here.


# 模型测试

# 视图测试
class AccountViewTests(TestCase):

    def test_index(self):
        response = client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_is_login(self):
        response = client.get('login.html', follow=True)
        self.assertRedirects(response, "/", status_code=302, target_status_code=200)

    def test_login_with_not_login(self):
        response = client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

