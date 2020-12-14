import random, string

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from . import models
from .forms import UserForm, RegisterForm
from search.forms import SearchForm, SmallSearchForm

# Create your views here.

def generate_code(num):
    return ''.join(random.sample(string.ascii_letters + string.digits, num))

def send_email(email, code):
    subject = '课评评注册激活邮件'
    text_content = '''感谢注册课评评，在这里你可以匿名地分享、吐槽课程，\
                      如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''<p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>课评评网站</a>，\
                    在这里你可以匿名地分享、吐槽课程！</p>
                    <p>请点击<a href="http://{}/confirm/?code={}" target=blank>这里</a>完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>'''.format(
                        '127.0.0.1:8000', 
                        code, 
                        '127.0.0.1:8000',
                        code,
                        settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()

def index(request):
    search_form = SearchForm()
    small_search_form = SmallSearchForm()
    return render(request, 'index.html', locals()) # 主页

def login(request):
    if request.session.get('is_login', None): # 是否已登录
        return redirect("/")

    if request.method == "POST": # POST请求处理
        login_form = UserForm(request.POST)
        message = "请检查输入内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(username=username)
                if check_password(password, user.password):
                    if user.is_active:
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.username
                        request.session['user_school'] = user.school.school_name
                        if login_form.cleaned_data['is_rem']:
                            request.session.set_expiry(7 * 24 * 3600) # 保存1周
                        else:
                            request.session.set_expiry(12 * 3600)
                        return redirect("/")
                    else:
                        message = "请先激活账号！"
                        # TODO: 此处增加一个重定向
                else:
                    message = "用户名或密码错误"
            except ObjectDoesNotExist:
                message = "用户名或密码错误"
        return render(request, 'account/login.html', locals())

    login_form = UserForm()
    return render(request, 'account/login.html', locals()) # 渲染登录界面

def logout(request):
    if not request.session.get('is_login', None): # 本身就没有登录，无需登出
        return redirect("/")

    request.session.flush()
    return redirect('/')

def register(request):
    if request.session.get('is_login', None): # 登录情况下不能注册
        return redirect("/")

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            password_confirm = register_form.cleaned_data['password_confirm']
            school = register_form.cleaned_data['school']
            email = register_form.cleaned_data['email']
            if password != password_confirm:
                message = "两次输入的密码不同！"
                return render(request, 'account/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'account/register.html', locals())

                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'account/register.html', locals())

                if school.email_addr != email.split("@")[-1]:
                    message = "邮箱域名错误！请使用本学校edu邮箱！"
                    return render(request, 'account/register.html', locals())

                models.User.objects.create(
                    username=username,
                    password=make_password(password),
                    email = email,
                    school = school)

                code = generate_code(30)
                send_email(email, code)
                models.EmailVerify.objects.create(email=email, code=code, send_type="r")

                return redirect('/confirm/')

    register_form = RegisterForm()
    return render(request, 'account/register.html', locals())

def confirm(request):
    if request.method == "GET":
        code = request.GET.get("code")
        try:
            right = models.EmailVerify.objects.get(code=code)
            if right.is_valid:
                right_user = models.User.objects.get(email=right.email)
                right_user.is_active = True
                right_user.save()
            else:
                return redirect('/register/')
        except ObjectDoesNotExist:
            pass
        return redirect('/login/')
    return redirect('/register/')

def userinfo(request):
    return render(request, 'account/userspace.html', locals())