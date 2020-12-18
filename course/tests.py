from django.test import TestCase
from django.test import Client
from django.urls import reverse
from account.models import User
from school.models import School, Department, Teacher
from course.models import Course, CourseTeacher
from comment.models import Comment
from vote.models import Vote
from django.contrib.auth.hashers import make_password, check_password

# create an instance of the client for our use
client = Client()


# Create your tests here.


# 模型测试
class CommentModelTests(TestCase):

    def test_course_comment_count(self):
        """
        计算课程的总评论数
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
        course_test = Course(course_name="course_test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        comment_test = Comment(course=course_test, user=user_test, content="yes!", zan=0, cai=0)
        comment_test.save()
        comment_test2 = Comment(course=course_test, user=user_test, content="yes!!", zan=0, cai=0)
        comment_test2.save()
        comment_test3 = Comment(course=course_test, user=user_test, content="yes!!!", zan=0, cai=0)
        comment_test3.save()
        comment_test4 = Comment(course=course_test, user=user_test, content="yes!!!！", zan=0, cai=0)
        comment_test4.save()
        self.assertEqual(course_test.comment_count(), 4)


# 视图测试
class CourseViewTests(TestCase):

    def test_add_course(self):
        """
        测试添加课程页面是否可以成功打开
        """
        response = client.get("/course/addcourse/")
        self.assertEqual(response.status_code, 200)

    def test_course_info(self):
        """
        测试课程信息页面是否可以成功打开
        """
        response = client.get("/course/1")
        self.assertEqual(response.status_code, 200)

    def test_change_course_info(self):
        """
        测试修改课程信息页面是否可以成功打开
        """
        response = client.get("/course/changecourseinfo/")
        self.assertEqual(response.status_code, 200)
