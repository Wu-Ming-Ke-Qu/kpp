from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from . import models
from .forms import UserForm, RegisterForm
from school.models import School

# Create your views here.

def index(request):
    return render(request, 'index.html') # 主页

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
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    if login_form.cleaned_data['is_rem']:
                        request.session.set_expiry(7 * 24 * 3600) # 保存1周
                    else:
                        request.session.set_expiry(12 * 3600)
                    return redirect("/")
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

                user_school = School.objects.get(pk=school)
                if user_school.email_addr != email.split("@")[-1]:
                    message = "邮箱域名错误！请使用本学校edu邮箱！"
                    return render(request, 'account/register.html', locals())

                new_user = models.User.objects.create(
                    username=username,
                    password=make_password(password),
                    email = email,
                    school = user_school)
                return redirect('/login/')

    register_form = RegisterForm()
    return render(request, 'account/register.html', locals())