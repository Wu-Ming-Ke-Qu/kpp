from django.test import TestCase
from account.models import User
from school.models import School, Department, Teacher
from course.models import Course, CourseTeacher
from comment.models import Comment
from vote.models import Vote
from django.contrib.auth.hashers import make_password, check_password

# Create your tests here.


# 模型测试
class CommentModelTests(TestCase):

    def test_comment_total_approve(self):
        """
        计算评论的总赞数
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        teacher_test = Teacher(teacher_name="li", school=school_test, department=department_test)
        teacher_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        user_test2 = User(username="user_test2", password=make_password("123456"), email="test2@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test2.save()
        user_test3 = User(username="user_test3", password=make_password("123456"), email="test3@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test3.save()
        course_test = Course(course_name="course_test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        comment_test = Comment(course=course_test, user=user_test, content="yes!", zan=0, cai=0)
        comment_test.save()
        vote_test = Vote(user=user_test, comment=comment_test, attr="A")
        vote_test.save()
        vote_test2 = Vote(user=user_test2, comment=comment_test, attr="A")
        vote_test2.save()
        vote_test3 = Vote(user=user_test3, comment=comment_test, attr="D")
        vote_test3.save()
        self.assertEqual(comment_test.total_approve(), 2)

    def test_comment_total_disapprove(self):
        """
        计算评论的总踩数
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        teacher_test = Teacher(teacher_name="li", school=school_test, department=department_test)
        teacher_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        user_test2 = User(username="user_test2", password=make_password("123456"), email="test2@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test2.save()
        user_test3 = User(username="user_test3", password=make_password("123456"), email="test3@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test3.save()
        user_test4 = User(username="user_test4", password=make_password("123456"), email="test4@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test4.save()
        course_test = Course(course_name="course_test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        comment_test = Comment(course=course_test, user=user_test, content="yes!", zan=0, cai=0)
        comment_test.save()
        vote_test = Vote(user=user_test, comment=comment_test, attr="A")
        vote_test.save()
        vote_test2 = Vote(user=user_test2, comment=comment_test, attr="D")
        vote_test2.save()
        vote_test3 = Vote(user=user_test3, comment=comment_test, attr="D")
        vote_test3.save()
        vote_test4 = Vote(user=user_test4, comment=comment_test, attr="D")
        vote_test4.save()
        self.assertEqual(comment_test.total_disapprove(), 3)

    def test_is_folded_with_bad_comment(self):
        """
        评论总赞数大于等于（总踩数-1）则不折叠
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        teacher_test = Teacher(teacher_name="li", school=school_test, department=department_test)
        teacher_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        user_test2 = User(username="user_test2", password=make_password("123456"), email="test2@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test2.save()
        # ...
        course_test = Course(course_name="course_test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        comment_test = Comment(course=course_test, user=user_test, content="yes!", zan=0, cai=0)
        comment_test.save()
        vote_test = Vote(user=user_test, comment=comment_test, attr="A")
        vote_test.save()
        vote_test2 = Vote(user=user_test2, comment=comment_test, attr="A")
        vote_test2.save()
        # ...
        self.assertIs(comment_test.is_folded(), True)

    def test_is_folded_with_good_comment(self):
        """
        评论总踩数大于（总赞数+1）则进行折叠
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        teacher_test = Teacher(teacher_name="li", school=school_test, department=department_test)
        teacher_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        user_test2 = User(username="user_test2", password=make_password("123456"), email="test2@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test2.save()
        # ...
        course_test = Course(course_name="course_test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        comment_test = Comment(course=course_test, user=user_test, content="yes!", zan=0, cai=0)
        comment_test.save()
        vote_test = Vote(user=user_test, comment=comment_test, attr="A")
        vote_test.save()
        vote_test2 = Vote(user=user_test2, comment=comment_test, attr="A")
        vote_test2.save()
        # ...
        self.assertIs(comment_test.is_folded(), False)

    def test_show_content_with_long_comment(self):
        """
        Comment如果评论内容长度大于10则展示评论概要（前10项）
        """
        long_comment = Comment(content="this is a long long long comment")
        self.assertEqual(long_comment.show_content(), "this is a ")

    def test_show_content_with_short_comment(self):
        """
        Comment如果评论内容长度小于10则展示评论内容
        """
        short_comment = Comment(content="short")
        self.assertEqual(short_comment.show_content(), "short")

# 视图测试
