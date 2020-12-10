from django.test import TestCase
from .models import Comment


# Create your tests here.

# 模型测试
class CommentModelTests(TestCase):

    def is_folded_with_bad_comment(self):
        """
        is_folded() returns True for comment which approve_count
        is less than disapprove_count.
        """
        bad_comment = Comment(approve_count=0, disapprove_count=1)
        self.assertIs(bad_comment.is_folded(), True)

    def is_folded_with_good_comment(self):
        """
        is_folded() returns False for comment which approve_count
        is more than disapprove_count.
        """
        good_comment = Comment(approve_count=1, disapprove_count=0)
        self.assertIs(good_comment.is_folded(), False)

    def show_content_with_long_comment(self):
        """
        show_content() returns self.content[:10] for comment which len(self.content)
        is more than 10.
        """
        long_comment = Comment(content="this is a long long long comment")
        self.assertIs(long_comment.show_content(), "this is a ")

    def show_content_with_short_comment(self):
        """
        show_content() returns self.content for comment which len(self.content)
        is not more than 10.
        """
        short_comment = Comment(content="short")
        self.assertIs(short_comment.show_content(), "short")

# 视图测试
