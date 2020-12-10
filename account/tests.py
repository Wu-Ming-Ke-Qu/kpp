import datetime
from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from .models import User
from .models import EmailVerify


# Create your tests here.


# 模型测试
class UserModelTests(TestCase):

    def test_is_new_user_with_future_user(self):
        """
        is_new_user() returns False for users whose ctime
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_user = User(ctime=time)
        self.assertIs(future_user.is_new_user(), False)

    def test_is_new_user_with_old_user(self):
        """
        is_new_user() returns False for users whose ctime
        is older than 30 days.
        """
        time = timezone.now() - datetime.timedelta(days=30, seconds=1)
        old_user = User(ctime=time)
        self.assertIs(old_user.is_new_user(), False)

    def test_is_new_user_with_new_user(self):
        """
        is_new_user() returns True for users whose ctime
        is within 30 days.
        """
        time = timezone.now() - datetime.timedelta(days=29, hours=23, minutes=59, seconds=59)
        new_user = User(ctime=time)
        self.assertIs(new_user.is_new_user(), True)


class EmailVerifyModelTests(TestCase):

    def test_is_valid_with_future_email(self):
        """
        is_valid() returns False for email whose ctime
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_email = EmailVerify(ctime=time)
        self.assertIs(future_email.is_valid(), False)

    def test_is_valid_with_old_email(self):
        """
        is_valid() returns False for email whose ctime
        is older than settings.CONFIRM_DAYS.
        """
        time = timezone.now() - datetime.timedelta(days=settings.CONFIRM_DAYS, seconds=1)
        old_email = EmailVerify(ctime=time)
        self.assertIs(old_email.is_valid(), False)

    def test_is_valid_with_recent_email(self):
        """
        is_valid() returns True for email whose ctime
        is within settings.CONFIRM_DAYS.
        """
        time = timezone.now() - datetime.timedelta(days=(settings.CONFIRM_DAYS - 1), hours=23, minutes=59, seconds=59)
        recent_email = EmailVerify(ctime=time)
        self.assertIs(recent_email.is_valid(), True)

# 视图测试
