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
