from django.db import models
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from school.models import School, Department, Teacher
from course.models import Course, CourseTeacher
from comment.models import Comment
from vote.models import Vote
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .models import EmailVerify

# create an instance of the client for our use
client = Client()


# Create your tests here.


# 模型测试
class AccountModelTests(TestCase):

    def test_user_total_approve(self):
        """
        计算用户发表评论得到的总赞数
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
        course_test = Course(course_name="course_test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        course_test2 = Course(course_name="course_test2", course_id="1234567", school=school_test,
                              department=department_test, credit=3, hour=64)
        course_test2.save()
        teacher_course2 = CourseTeacher(course=course_test2, teacher=teacher_test)
        teacher_course2.save()
        comment_test = Comment(course=course_test, user=user_test, content="yes!", zan=0, cai=0)
        comment_test.save()
        comment_test2 = Comment(course=course_test2, user=user_test, content="yes!!!", zan=0, cai=0)
        comment_test2.save()
        vote_test = Vote(user=user_test, comment=comment_test, attr="A")
        vote_test.save()
        vote_test2 = Vote(user=user_test2, comment=comment_test, attr="A")
        vote_test2.save()
        vote_test3 = Vote(user=user_test2, comment=comment_test2, attr="A")
        vote_test3.save()
        self.assertEqual(user_test.total_approve(), 3)

    def test_user_total_disapprove(self):
        """
        计算用户发表评论得到的总踩数
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
        course_test = Course(course_name="course_test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        course_test2 = Course(course_name="course_test2", course_id="1234567", school=school_test,
                              department=department_test, credit=3, hour=64)
        course_test2.save()
        teacher_course2 = CourseTeacher(course=course_test2, teacher=teacher_test)
        teacher_course2.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        comment_test = Comment(course=course_test, user=user_test, content="yes!", zan=0, cai=0)
        comment_test.save()
        comment_test2 = Comment(course=course_test2, user=user_test, content="yes!!!", zan=0, cai=0)
        comment_test2.save()
        vote_test = Vote(user=user_test, comment=comment_test, attr="D")
        vote_test.save()
        vote_test2 = Vote(user=user_test2, comment=comment_test, attr="D")
        vote_test2.save()
        vote_test3 = Vote(user=user_test2, comment=comment_test2, attr="D")
        vote_test3.save()
        self.assertEqual(user_test.total_disapprove(), 3)


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
