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
        self.assertEqual(comment_test.approve_count(), 2)

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
        self.assertEqual(comment_test.disapprove_count(), 3)

    def test_is_folded_with_comment_case1(self):
        """
        评论（总赞数+总踩数）大于等于20且总踩数/（总赞数+总踩数）大于等于0.7则进行折叠
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
        user_test5 = User(username="user_test5", password=make_password("123456"), email="test5@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test5.save()
        user_test6 = User(username="user_test6", password=make_password("123456"), email="test6@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test6.save()
        user_test7 = User(username="user_test7", password=make_password("123456"), email="test7@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test7.save()
        user_test8 = User(username="user_test8", password=make_password("123456"), email="test8@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test8.save()
        user_test9 = User(username="user_test9", password=make_password("123456"), email="test9@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test9.save()
        user_test10 = User(username="user_test10", password=make_password("123456"), email="test10@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test10.save()
        user_test11 = User(username="user_test11", password=make_password("123456"), email="test11@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test11.save()
        user_test12 = User(username="user_test12", password=make_password("123456"), email="test12@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test12.save()
        user_test13 = User(username="user_test13", password=make_password("123456"), email="test13@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test13.save()
        user_test14 = User(username="user_test14", password=make_password("123456"), email="test14@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test14.save()
        user_test15 = User(username="user_test15", password=make_password("123456"), email="test15@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test15.save()
        user_test16 = User(username="user_test16", password=make_password("123456"), email="test16@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test16.save()
        user_test17 = User(username="user_test17", password=make_password("123456"), email="test17@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test17.save()
        user_test18 = User(username="user_test18", password=make_password("123456"), email="test18@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test18.save()
        user_test19 = User(username="user_test19", password=make_password("123456"), email="test19@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test19.save()
        user_test20 = User(username="user_test20", password=make_password("123456"), email="test20@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test20.save()
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
        vote_test3 = Vote(user=user_test3, comment=comment_test, attr="A")
        vote_test3.save()
        vote_test4 = Vote(user=user_test4, comment=comment_test, attr="A")
        vote_test4.save()
        vote_test5 = Vote(user=user_test5, comment=comment_test, attr="A")
        vote_test5.save()
        vote_test6 = Vote(user=user_test6, comment=comment_test, attr="A")
        vote_test6.save()
        vote_test7 = Vote(user=user_test7, comment=comment_test, attr="D")
        vote_test7.save()
        vote_test8 = Vote(user=user_test8, comment=comment_test, attr="D")
        vote_test8.save()
        vote_test9 = Vote(user=user_test9, comment=comment_test, attr="D")
        vote_test9.save()
        vote_test10 = Vote(user=user_test10, comment=comment_test, attr="D")
        vote_test10.save()
        vote_test11 = Vote(user=user_test11, comment=comment_test, attr="D")
        vote_test11.save()
        vote_test12 = Vote(user=user_test12, comment=comment_test, attr="D")
        vote_test12.save()
        vote_test13 = Vote(user=user_test13, comment=comment_test, attr="D")
        vote_test13.save()
        vote_test14 = Vote(user=user_test14, comment=comment_test, attr="D")
        vote_test14.save()
        vote_test15 = Vote(user=user_test15, comment=comment_test, attr="D")
        vote_test15.save()
        vote_test16 = Vote(user=user_test16, comment=comment_test, attr="D")
        vote_test16.save()
        vote_test17 = Vote(user=user_test17, comment=comment_test, attr="D")
        vote_test17.save()
        vote_test18 = Vote(user=user_test18, comment=comment_test, attr="D")
        vote_test18.save()
        vote_test19 = Vote(user=user_test19, comment=comment_test, attr="D")
        vote_test19.save()
        vote_test20 = Vote(user=user_test20, comment=comment_test, attr="D")
        vote_test20.save()
        self.assertIs(comment_test.is_folded(), True)

    def test_is_folded_with_comment_case2(self):
        """
        评论（总赞数+总踩数）小于20且总踩数大于等于14则进行折叠
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
        user_test5 = User(username="user_test5", password=make_password("123456"), email="test5@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test5.save()
        user_test6 = User(username="user_test6", password=make_password("123456"), email="test6@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test6.save()
        user_test7 = User(username="user_test7", password=make_password("123456"), email="test7@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test7.save()
        user_test8 = User(username="user_test8", password=make_password("123456"), email="test8@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test8.save()
        user_test9 = User(username="user_test9", password=make_password("123456"), email="test9@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test9.save()
        user_test10 = User(username="user_test10", password=make_password("123456"), email="test10@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test10.save()
        user_test11 = User(username="user_test11", password=make_password("123456"), email="test11@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test11.save()
        user_test12 = User(username="user_test12", password=make_password("123456"), email="test12@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test12.save()
        user_test13 = User(username="user_test13", password=make_password("123456"), email="test13@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test13.save()
        user_test14 = User(username="user_test14", password=make_password("123456"), email="test14@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test14.save()
        user_test15 = User(username="user_test15", password=make_password("123456"), email="test15@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test15.save()
        user_test16 = User(username="user_test16", password=make_password("123456"), email="test16@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test16.save()
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
        vote_test4 = Vote(user=user_test4, comment=comment_test, attr="D")
        vote_test4.save()
        vote_test5 = Vote(user=user_test5, comment=comment_test, attr="D")
        vote_test5.save()
        vote_test6 = Vote(user=user_test6, comment=comment_test, attr="D")
        vote_test6.save()
        vote_test7 = Vote(user=user_test7, comment=comment_test, attr="D")
        vote_test7.save()
        vote_test8 = Vote(user=user_test8, comment=comment_test, attr="D")
        vote_test8.save()
        vote_test9 = Vote(user=user_test9, comment=comment_test, attr="D")
        vote_test9.save()
        vote_test10 = Vote(user=user_test10, comment=comment_test, attr="D")
        vote_test10.save()
        vote_test11 = Vote(user=user_test11, comment=comment_test, attr="D")
        vote_test11.save()
        vote_test12 = Vote(user=user_test12, comment=comment_test, attr="D")
        vote_test12.save()
        vote_test13 = Vote(user=user_test13, comment=comment_test, attr="D")
        vote_test13.save()
        vote_test14 = Vote(user=user_test14, comment=comment_test, attr="D")
        vote_test14.save()
        vote_test15 = Vote(user=user_test15, comment=comment_test, attr="D")
        vote_test15.save()
        vote_test16 = Vote(user=user_test16, comment=comment_test, attr="D")
        vote_test16.save()
        self.assertIs(comment_test.is_folded(), True)

    def test_is_folded_with_comment_case3(self):
        """
        评论（总赞数+总踩数）小于20且总踩数/（总赞数+总踩数）大于等于0.7但总踩数小于14则不进行折叠
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
        user_test5 = User(username="user_test5", password=make_password("123456"), email="test5@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test5.save()
        user_test6 = User(username="user_test6", password=make_password("123456"), email="test6@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test6.save()
        user_test7 = User(username="user_test7", password=make_password("123456"), email="test7@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test7.save()
        user_test8 = User(username="user_test8", password=make_password("123456"), email="test8@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test8.save()
        user_test9 = User(username="user_test9", password=make_password("123456"), email="test9@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test9.save()
        user_test10 = User(username="user_test10", password=make_password("123456"), email="test10@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test10.save()
        user_test11 = User(username="user_test11", password=make_password("123456"), email="test11@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test11.save()
        user_test12 = User(username="user_test12", password=make_password("123456"), email="test12@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test12.save()
        user_test13 = User(username="user_test13", password=make_password("123456"), email="test13@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test13.save()
        user_test14 = User(username="user_test14", password=make_password("123456"), email="test14@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test14.save()
        user_test15 = User(username="user_test15", password=make_password("123456"), email="test15@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test15.save()
        user_test16 = User(username="user_test16", password=make_password("123456"), email="test16@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test16.save()
        course_test = Course(course_name="course_test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        comment_test = Comment(course=course_test, user=user_test, content="yes!", zan=0, cai=0)
        comment_test.save()
        vote_test = Vote(user=user_test, comment=comment_test, attr="D")
        vote_test.save()
        vote_test2 = Vote(user=user_test2, comment=comment_test, attr="D")
        vote_test2.save()
        vote_test3 = Vote(user=user_test3, comment=comment_test, attr="D")
        vote_test3.save()
        vote_test4 = Vote(user=user_test4, comment=comment_test, attr="D")
        vote_test4.save()
        vote_test5 = Vote(user=user_test5, comment=comment_test, attr="D")
        vote_test5.save()
        vote_test6 = Vote(user=user_test6, comment=comment_test, attr="D")
        vote_test6.save()
        vote_test7 = Vote(user=user_test7, comment=comment_test, attr="D")
        vote_test7.save()
        vote_test8 = Vote(user=user_test8, comment=comment_test, attr="D")
        vote_test8.save()
        vote_test9 = Vote(user=user_test9, comment=comment_test, attr="D")
        vote_test9.save()
        vote_test10 = Vote(user=user_test10, comment=comment_test, attr="D")
        vote_test10.save()
        vote_test11 = Vote(user=user_test11, comment=comment_test, attr="D")
        vote_test11.save()
        vote_test12 = Vote(user=user_test12, comment=comment_test, attr="D")
        vote_test12.save()
        vote_test13 = Vote(user=user_test13, comment=comment_test, attr="D")
        vote_test13.save()
        vote_test14 = Vote(user=user_test14, comment=comment_test, attr="A")
        vote_test14.save()
        vote_test15 = Vote(user=user_test15, comment=comment_test, attr="A")
        vote_test15.save()
        vote_test16 = Vote(user=user_test16, comment=comment_test, attr="A")
        vote_test16.save()
        self.assertIs(comment_test.is_folded(), False)

    def test_is_folded_with_comment_case4(self):
        """
        评论（总赞数+总踩数）大于等于20且总踩数/（总赞数+总踩数）小于0.7则不进行折叠
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
        user_test5 = User(username="user_test5", password=make_password("123456"), email="test5@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test5.save()
        user_test6 = User(username="user_test6", password=make_password("123456"), email="test6@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test6.save()
        user_test7 = User(username="user_test7", password=make_password("123456"), email="test7@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test7.save()
        user_test8 = User(username="user_test8", password=make_password("123456"), email="test8@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test8.save()
        user_test9 = User(username="user_test9", password=make_password("123456"), email="test9@126.com",
                          school=school_test, department=department_test, is_active=True)
        user_test9.save()
        user_test10 = User(username="user_test10", password=make_password("123456"), email="test10@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test10.save()
        user_test11 = User(username="user_test11", password=make_password("123456"), email="test11@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test11.save()
        user_test12 = User(username="user_test12", password=make_password("123456"), email="test12@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test12.save()
        user_test13 = User(username="user_test13", password=make_password("123456"), email="test13@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test13.save()
        user_test14 = User(username="user_test14", password=make_password("123456"), email="test14@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test14.save()
        user_test15 = User(username="user_test15", password=make_password("123456"), email="test15@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test15.save()
        user_test16 = User(username="user_test16", password=make_password("123456"), email="test16@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test16.save()
        user_test17 = User(username="user_test17", password=make_password("123456"), email="test17@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test17.save()
        user_test18 = User(username="user_test18", password=make_password("123456"), email="test18@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test18.save()
        user_test19 = User(username="user_test19", password=make_password("123456"), email="test19@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test19.save()
        user_test20 = User(username="user_test20", password=make_password("123456"), email="test20@126.com",
                           school=school_test, department=department_test, is_active=True)
        user_test20.save()
        course_test = Course(course_name="course_test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        comment_test = Comment(course=course_test, user=user_test, content="yes!", zan=0, cai=0)
        comment_test.save()
        vote_test = Vote(user=user_test, comment=comment_test, attr="D")
        vote_test.save()
        vote_test2 = Vote(user=user_test2, comment=comment_test, attr="D")
        vote_test2.save()
        vote_test3 = Vote(user=user_test3, comment=comment_test, attr="D")
        vote_test3.save()
        vote_test4 = Vote(user=user_test4, comment=comment_test, attr="D")
        vote_test4.save()
        vote_test5 = Vote(user=user_test5, comment=comment_test, attr="D")
        vote_test5.save()
        vote_test6 = Vote(user=user_test6, comment=comment_test, attr="D")
        vote_test6.save()
        vote_test7 = Vote(user=user_test7, comment=comment_test, attr="D")
        vote_test7.save()
        vote_test8 = Vote(user=user_test8, comment=comment_test, attr="D")
        vote_test8.save()
        vote_test9 = Vote(user=user_test9, comment=comment_test, attr="D")
        vote_test9.save()
        vote_test10 = Vote(user=user_test10, comment=comment_test, attr="D")
        vote_test10.save()
        vote_test11 = Vote(user=user_test11, comment=comment_test, attr="D")
        vote_test11.save()
        vote_test12 = Vote(user=user_test12, comment=comment_test, attr="D")
        vote_test12.save()
        vote_test13 = Vote(user=user_test13, comment=comment_test, attr="D")
        vote_test13.save()
        vote_test14 = Vote(user=user_test14, comment=comment_test, attr="A")
        vote_test14.save()
        vote_test15 = Vote(user=user_test15, comment=comment_test, attr="A")
        vote_test15.save()
        vote_test16 = Vote(user=user_test16, comment=comment_test, attr="A")
        vote_test16.save()
        vote_test17 = Vote(user=user_test17, comment=comment_test, attr="A")
        vote_test17.save()
        vote_test18 = Vote(user=user_test18, comment=comment_test, attr="A")
        vote_test18.save()
        vote_test19 = Vote(user=user_test19, comment=comment_test, attr="A")
        vote_test19.save()
        vote_test20 = Vote(user=user_test20, comment=comment_test, attr="A")
        vote_test20.save()
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

