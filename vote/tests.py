import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Vote


# Create your tests here.


# 模型测试
class UserModelTests(TestCase):

    def is_recent_vote_with_future_vote(self):
        """
        is_recent_vote() returns False for votes whose ctime
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_vote = Vote(ch_time=time)
        self.assertIs(future_vote.is_recent_vote(), False)

    def is_recent_vote_with_past_vote(self):
        """
        is_recent_vote() returns False for votes whose ctime
        is older than 3 days.
        """
        time = timezone.now() - datetime.timedelta(days=3, seconds=1)
        past_vote = Vote(ch_time=time)
        self.assertIs(past_vote.is_recent_vote(), False)

    def is_recent_vote_with_recent_vote(self):
        """
        is_recent_vote() returns True for votes whose ctime
        is within 3 days.
        """
        time = timezone.now() - datetime.timedelta(days=2, hours=23, minutes=59, seconds=59)
        recent_vote = Vote(ch_time=time)
        self.assertIs(recent_vote.is_recent_vote(), True)

# 视图测试
