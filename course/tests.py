from django.test import TestCase
from django.test import Client
from account.models import User
from school.models import School, Department, Teacher
from course.models import Course, CourseTeacher
from comment.models import Comment
from django.contrib.auth.hashers import make_password

# create an instance of the client for our use
client = Client()


# Create your tests here.


# 模型测试
class CourseModelTests(TestCase):

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

    def test_addcourse(self):
        """
        测试添加课程页面是否可以成功打开
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.get("/course/addcourse/")
        self.assertEqual(response.status_code, 200)

    def test_addcourse_with_not_login(self):
        """
        未登录状态无法添加课程
        并重定向到login页面
        """
        response = client.get("/course/addcourse/")
        self.assertRedirects(response, "/login/", status_code=302, target_status_code=200)

    def test_addcourse_with_is_login_add_successful(self):
        """
        登录状态下成功添加课程
        则重定向到相应的课程信息页面
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.post('/course/addcourse/', {'course_name': 'course_test', 'course_id': '123456',
                                                      'school': school_test.id, 'department': 'de_test',
                                                      'teacher': "li", 'credit': 3, 'hour': 64, 'pre_course': "pre"})
        self.assertRedirects(response, "/course/" + str(1), status_code=302, target_status_code=200)

    def test_addcourse_with_is_login_same_course_id(self):
        """
        登录状态下添加课程如已经存在相同课程号
        则返回message"存在课程号相同的课程！"
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
        course_test = Course(course_name="test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.post('/course/addcourse/', {'course_name': 'course_test', 'course_id': '123456',
                                                      'school': school_test.id, 'department': 'de_test',
                                                      'teacher': "li", 'credit': 3, 'hour': 64, 'pre_course': "pre"})
        self.assertEqual(response.context['message'], "存在课程号相同的课程！")
        self.assertEqual(response.status_code, 200)

    def test_addcourse_with_wrong_course_form1(self):
        """
        添加课程输入格式错误-没有输入课程名
        则返回message"请检查填写的内容！"
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.post('/course/addcourse/', {'course_id': '123456', 'school': school_test.id,
                                                      'department': 'de_test', 'teacher': "li", 'credit': 3,
                                                      'hour': 64, 'pre_course': "pre"})
        self.assertEqual(response.context['message'], "请检查填写的内容！")
        self.assertEqual(response.status_code, 200)

    def test_addcourse_with_wrong_course_form2(self):
        """
        添加课程输入格式错误-没有选择学校
        则返回message"请检查填写的内容！"
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.post('/course/addcourse/', {'course_name': 'course_test', 'course_id': '123456',
                                                      'department': 'de_test', 'teacher': "li", 'credit': 3,
                                                      'hour': 64, 'pre_course': "pre"})
        self.assertEqual(response.context['message'], "请检查填写的内容！")
        self.assertEqual(response.status_code, 200)

    def test_addcourse_with_wrong_course_form3(self):
        """
        添加课程输入格式错误-没有输入院系
        则返回message"请检查填写的内容！"
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.post('/course/addcourse/', {'course_name': 'course_test', 'course_id': '123456',
                                                      'school': school_test.id, 'teacher': "li", 'credit': 3,
                                                      'hour': 64, 'pre_course': "pre"})
        self.assertEqual(response.context['message'], "请检查填写的内容！")
        self.assertEqual(response.status_code, 200)

    def test_addcourse_with_wrong_course_form4(self):
        """
        添加课程输入格式错误-没有输入任课教师
        则返回message"请检查填写的内容！"
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.post('/course/addcourse/', {'course_name': 'course_test', 'course_id': '123456',
                                                      'school': school_test.id, 'department': 'de_test',
                                                      'credit': 3, 'hour': 64, 'pre_course': "pre"})
        self.assertEqual(response.context['message'], "请检查填写的内容！")
        self.assertEqual(response.status_code, 200)

    def test_addcourse_with_wrong_course_form5(self):
        """
        添加课程输入格式错误-没有输入学分
        则返回message"请检查填写的内容！"
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.post('/course/addcourse/', {'course_name': 'course_test', 'course_id': '123456',
                                                      'school': school_test.id, 'department': 'de_test',
                                                      'teacher': "li", 'hour': 64, 'pre_course': "pre"})
        self.assertEqual(response.context['message'], "请检查填写的内容！")
        self.assertEqual(response.status_code, 200)

    def test_addcourse_with_wrong_course_form6(self):
        """
        添加课程输入格式错误-没有输入课程名
        则返回message"请检查填写的内容！"
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.post('/course/addcourse/', {'course_name': 'course_test', 'course_id': '123456',
                                                      'school': school_test.id, 'department': 'de_test',
                                                      'teacher': "li", 'credit': 3, 'pre_course': "pre"})
        self.assertEqual(response.context['message'], "请检查填写的内容！")
        self.assertEqual(response.status_code, 200)

    def test_course_info(self):
        """
        测试课程信息页面是否可以成功打开
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        teacher_test = Teacher(teacher_name="li", school=school_test, department=department_test)
        teacher_test.save()
        course_test = Course(course_name="test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        response = client.get("/course/1")
        self.assertEqual(response.status_code, 200)

    def test_change_course_info(self):
        """
        测试修改课程信息页面是否可以成功打开
        """
        school_test = School(school_name="thu")
        school_test.save()
        department_test = Department(department_name="ce", school=school_test)
        department_test.save()
        teacher_test = Teacher(teacher_name="li", school=school_test, department=department_test)
        teacher_test.save()
        course_test = Course(course_name="test", course_id="123456", school=school_test,
                             department=department_test, credit=3, hour=64)
        course_test.save()
        teacher_course = CourseTeacher(course=course_test, teacher=teacher_test)
        teacher_course.save()
        user_test = User(username="user_test", password=make_password("123456"), email="test@126.com",
                         school=school_test, department=department_test, is_active=True)
        user_test.save()
        client.post('/login/', {'username': 'user_test', 'password': '123456', 'is_rem': True})
        response = client.get("/course/changecourseinfo/1")
        self.assertEqual(response.status_code, 200)
