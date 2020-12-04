from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm

# Create your views here.

def index(request):
    pass
    return render(request, 'index.html')

def login(request):
    if request.session.get('is_login', None):
        return redirect("/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查输入内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect("/")
                else:
                    message = "用户名或密码错误"
            except:
                message = "用户名或密码错误"
        return render(request, 'account/login.html', locals())

    login_form = UserForm()
    return render(request, 'account/login.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    request.session.flush()
    return redirect('/')

def register(request):
    if request.session.get('is_login', None):
        return redirect("/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            password_confirm = register_form.cleaned_data['password_confirm']
            email = register_form.cleaned_data['email']
            if password != password_confirm:
                message = "两次输入的密码不同！"
                return render(request, 'account/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'account/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'account/register.html', locals())

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password
                new_user.email = email
                new_user.save()
                return redirect('/login/')
    register_form = RegisterForm()
    return render(request, 'account/register.html', locals())