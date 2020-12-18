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
        """
        测试index页面是否可以成功打开
        """
        response = client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """
        测试login页面是否可以成功打开
        """
        response = client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_is_login(self):
        """
        如果已经登陆则重新定向到主页面
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.get(reverse("login"))
        self.assertRedirects(response, "/", status_code=302, target_status_code=200)

    def test_login_with_login_successful(self):
        """
        如果未登陆则读取用户输入的数据
        成功登录后重新定向到主页面
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        response = client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        self.assertRedirects(response, "/", status_code=302, target_status_code=200)

    def test_login_with_user_is_not_active(self):
        """
        如果未登陆则读取用户输入的数据
        如果该用户未激活则返回message"请先激活账号!"
        并重定向到激活页面
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=False)
        user_test.save()
        response = client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        self.assertEqual(response.context['message'], "请先激活账号!")
        # self.assertRedirects(response, "/", status_code=302, target_status_code=200)

    def test_login_with_username_not_exist(self):
        """
        如果未登陆则读取用户输入的数据
        如果用户名不存在则返回message"用户名或密码错误"
        """
        response = client.post('/login/', {'username': 'user', 'password': '123456', 'is_rem': True})
        self.assertEqual(response.context['message'], "用户名或密码错误")
        self.assertEqual(response.status_code, 200)

    def test_login_with_wrong_password(self):
        """
        如果未登陆则读取用户输入的数据
        如果密码错误则返回message"用户名或密码错误"
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        response = client.post('/login/', {'username': 'user_test', 'password': '12345', 'is_rem': True})
        self.assertEqual(response.context['message'], "用户名或密码错误")
        self.assertEqual(response.status_code, 200)

    def test_login_with_wrong_login_form_no_password(self):
        """
        如果没有输入密码则输入格式不正确
        返回message"请检查输入内容！"
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        response = client.post('/login/', {'username': 'user_test', 'is_rem': True})
        self.assertEqual(response.context['message'], "请检查输入内容！")
        self.assertEqual(response.status_code, 200)

    def test_login_with_wrong_login_form_no_username(self):
        """
        如果没有输入账号则输入格式不正确
        返回message"请检查输入内容！"
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        response = client.post('/login/', {'password': '123456', 'is_rem': True})
        self.assertEqual(response.context['message'], "请检查输入内容！")
        self.assertEqual(response.status_code, 200)

    def test_logout_with_is_login(self):
        """
        如果已登录则登出
        并重定向到主页面
        进行验证是否成功登出
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.get(reverse("login"))
        self.assertRedirects(response, "/", status_code=302, target_status_code=200)
        response = client.get(reverse("logout"))
        self.assertRedirects(response, "/", status_code=302, target_status_code=200)
        response = client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_with_not_login(self):
        """
        如果本身没有登录
        则重定向到主页面
        """
        response = client.get(reverse("logout"))
        self.assertRedirects(response, "/", status_code=302, target_status_code=200)

    def test_register(self):
        """
        测试注册页面是否可以成功打开
        """
        response = client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_with_is_login(self):
        """
        如果已登录则无法注册
        并重定向到主页面
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.get(reverse("register"))
        self.assertRedirects(response, "/", status_code=302, target_status_code=200)

    def test_register_with_register_successful(self):
        """
        如果未登陆则读取用户输入的数据
        成功注册后重新定向到confirm界面
        """
        school_test = School(school_name="thu", email_addr="126.com")
        school_test.save()
        response = client.post('/register/', {'username': 'user_test', 'password': '123456',
                                              'password_confirm': '123456', 'school': school_test.id,
                                              'email': 'test@126.com'})
        self.assertEqual(response.context['message'], "两次输入的密码不同！")
        self.assertRedirects(response, "/confirm/", status_code=302, target_status_code=200)

    def test_register_with_wrong_password(self):
        """
        如果注册时两次填写的密码不相同
        返回message"两次输入的密码不同！"
        """
        school_test = School(school_name="thu", email_addr="126.com")
        school_test.save()
        response = client.post('/register/', {'username': 'user_test', 'password': '123456',
                                              'password_confirm': '12345', 'school': 'thu',
                                              'email': 'test@126.com'})
        self.assertEqual(response.context['message'], "两次输入的密码不同！")
        self.assertEqual(response.status_code, 200)

    def test_register_with_same_username(self):
        """
        如果用户名已经存在
        返回message"用户已经存在，请重新选择用户名！"
        """
        school_test = School(school_name="thu", email_addr="126.com")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        response = client.post('/register/', {'username': 'user_test', 'password': '123456',
                                              'password_confirm': '123456', 'school': 'thu',
                                              'email': 'ttest@126.com'})
        self.assertEqual(response.context['message'], "用户已经存在，请重新选择用户名！")
        self.assertEqual(response.status_code, 200)

    def test_register_with_same_email(self):
        """
        如果邮箱已经存在
        返回message"该邮箱地址已被注册，请使用别的邮箱！"
        """
        school_test = School(school_name="thu", email_addr="126.com")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        response = client.post('/register/', {'username': 'user', 'password': '123456',
                                              'password_confirm': '123456', 'school': 'thu',
                                              'email': 'test@126.com'})
        self.assertEqual(response.context['message'], "该邮箱地址已被注册，请使用别的邮箱！")
        self.assertEqual(response.status_code, 200)

    def test_register_with_wrong_email(self):
        """
        如果邮箱域名与学校邮箱域名不一样
        返回message"邮箱域名错误！请使用本学校edu邮箱！"
        """
        school_test = School(school_name="thu", email_addr="126.com")
        school_test.save()
        response = client.post('/register/', {'username': 'user_test', 'password': '123456',
                                              'password_confirm': '123456', 'school': 'thu',
                                              'email': 'test@163.com'})
        self.assertEqual(response.context['message'], "邮箱域名错误！请使用本学校edu邮箱！")
        self.assertEqual(response.status_code, 200)

    def test_register_with_wrong_register_form(self):
        """
        如果输入格式错误
        返回message"请检查填写的内容！"
        """
        school_test = School(school_name="thu", email_addr="126.com")
        school_test.save()
        response = client.post('/register/', {'username': 'user_test', 'password': '123456',
                                              'password_confirm': '123456', 'school': 'thu',
                                              'email': 'test@126.com'})
        self.assertEqual(response.context['message'], "请检查填写的内容！")
        self.assertEqual(response.status_code, 200)
