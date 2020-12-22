import random, string

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMultiAlternatives, message
from django.conf import settings

from . import models
from .forms import ChangePWForm, FindPWForm, ForgetPWForm, UserForm, RegisterForm
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

def send_forgetpw_email(email, code):
    subject = '课评评网站找回密码'
    text_content = '''感谢您使用课评评，在这里你可以匿名地分享、吐槽课程，\
                      如果您看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''<p>感谢您使用<a href="http://{}/account/findpw/?code={}" target=blank>课评评网站</a>，\
                    在这里你可以匿名地分享、吐槽课程！</p>
                    <p>请点击<a href="http://{}/account/findpw/?code={}" target=blank>这里</a>完成密码找回！</p>
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

    earch_form = SearchForm()
    small_search_form = SmallSearchForm()

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
                        message = "请先激活账号!"
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.username
                        request.session['user_school'] = user.school.school_name
                        return redirect("/account/emailcert/")
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

    search_form = SearchForm()
    small_search_form = SmallSearchForm()

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

            user = models.User.objects.create(
                username=username,
                password=make_password(password),
                email = email,
                school = school)
            
            code = generate_code(30)
            models.EmailVerify.objects.create(email=email, code=code, send_type="r")
            send_email(email, code)
            
            request.session['user_id'] = user.id
            request.session['user_name'] = user.username
            request.session['user_school'] = user.school.school_name

            return redirect('/account/emailcert/')
        return render(request, 'account/register.html', locals())

    register_form = RegisterForm()
    return render(request, 'account/register.html', locals())

def confirm(request):
    if request.method == "GET":
        code = request.GET.get("code")
        try:
            right = models.EmailVerify.objects.get(code=code)
            if right.is_valid():
                right_user = models.User.objects.get(email=right.email)
                right_user.is_active = True
                right_user.save()
                request.session['is_login'] = True
                request.session['user_id'] = right_user.id
                request.session['user_name'] = right_user.username
                request.session['user_school'] = right_user.school.school_name
                right.delete()
                return redirect('/account/certisuccess/')
            else:
                right_user = models.User.objects.get(email=right.email)
                request.session['user_id'] = right_user.id
                request.session['user_name'] = right_user.username
                request.session['user_school'] = right_user.school.school_name
                right.delete()
                return redirect('/account/emailcert/')
        except ObjectDoesNotExist:
            pass
        return redirect('/login/')
    
    search_form = SearchForm()
    small_search_form = SmallSearchForm()

    return render(request, "account/emailcerti.html", locals())

def certi_success(request):
    search_form = SearchForm()
    small_search_form = SmallSearchForm()
    return render(request, 'account/certisuccess.html', locals())

def userinfo(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")

    user = models.User.objects.get(pk = request.session["user_id"])
    search_form = SearchForm()
    small_search_form = SmallSearchForm()

    comment_list = []
    for comment in user.comment_set.all():
        comment_list.append(comment)

    return render(request, 'account/userspace.html', locals())

def email_cert(request):
    if request.session.get('is_login', None): # 激活情况下不能再激活
        return redirect("/")

    user_id = request.session.get('user_id', None)
    if user_id is not None:
        user = models.User.objects.get(pk=user_id)
        email_addr = user.email

    search_form = SearchForm()
    small_search_form = SmallSearchForm()

    return render(request, 'account/emailcerti.html', locals())

def send_email_again(request):
    if request.session.get('is_login', None): # 激活情况下不能再激活
        return redirect("/")
    
    user_id = request.session.get('user_id', None)
    email_addr = None
    if user_id is not None:
        user = models.User.objects.get(pk=user_id)
        email_addr = user.email
    if email_addr is None:
        return redirect('/login/')
    else:
        code = generate_code(30)
        models.EmailVerify.objects.create(email=email_addr, code=code, send_type="r")
        send_email(email_addr, code)
        return redirect("/")

def change_passwd(request):
    if not request.session.get('is_login', None):
        return redirect("/")

    search_form = SearchForm()
    small_search_form = SmallSearchForm()

    user = models.User.objects.get(pk=request.session['user_id'])

    if request.method == "POST":
        changepw_form = ChangePWForm(request.POST)
        message = "请检查填写的内容！"

        if changepw_form.is_valid():
            old_password = changepw_form.cleaned_data['old_password']
            new_password = changepw_form.cleaned_data['new_password']
            confirm_password = changepw_form.cleaned_data['confirm_password']
            if check_password(old_password, user.password):
                if old_password == new_password:
                    message = "新密码不能与旧密码相同！"
                    return render(request, 'account/changepw.html', locals())
                if new_password != confirm_password:
                    message = "两次输入的密码不同！"
                    return render(request, 'account/changepw.html', locals())
                
                user.password = make_password(new_password)
                user.save()
                return redirect("/account/")
            else:
                message = "密码错误！"
                return render(request, 'account/changepw.html', locals())
        else:
            return render(request, 'account/changepw.html', locals())

    changepw_form = ChangePWForm()
    return render(request, 'account/changepw.html', locals())

def forget_passwd(request):
    if request.session.get('is_login', None):
        return redirect("/")

    search_form = SearchForm()
    small_search_form = SmallSearchForm()

    if request.method == "POST":
        forgetpw_form = ForgetPWForm(request.POST)
        message = "请检查填写的内容！"
        if forgetpw_form.is_valid():
            email_addr = forgetpw_form.cleaned_data['email_addr']
            try:
                user = models.User.objects.get(email=email_addr)
                code = generate_code(30)
                models.EmailVerify.objects.create(email=email_addr, code=code, send_type="f")
                send_forgetpw_email(email_addr, code)
                message = "邮件已发送，请移步到收件箱继续操作！"
                return render(request, 'account/pwforget.html', locals())
            except ObjectDoesNotExist:
                message = "该邮箱未注册！"
                return render(request, 'account/pwforget.html', locals())
        else:
            return render(request, 'account/pwforget.html', locals()) 

    forgetpw_form = ForgetPWForm()
    return render(request, 'account/pwforget.html', locals()) 

def find_passwd(request):
    if request.session.get('is_login', None):
        return redirect("/")
    
    search_form = SearchForm()
    small_search_form = SmallSearchForm()

    if request.method == "POST":
        findpw_form = FindPWForm(request.POST)
        message = "请检查填写的内容！"
        if findpw_form.is_valid():
            new_password = findpw_form.cleaned_data['new_password']
            confirm_password = findpw_form.cleaned_data['confirm_password']
            if new_password != confirm_password:
                message = "两次输入密码不同！"
                return redirect("/account/forgetpw/")
            
            code = request.POST['code']
            target = models.EmailVerify.objects.get(code=code)
            if target.is_valid():
                user = models.User.objects.get(email=target.email)
                user.password = make_password(new_password)
                user.save()
                target.delete()
                return redirect("/login/")
            else:
                target.delete()
                return redirect("/account/forgetpw/")
        else:
            return redirect("/account/forgetpw/")

    if request.method == "GET":
        try:
            code = request.GET['code']
        except Exception:
            return redirect("/login/")
        try:
            target = models.EmailVerify.objects.get(code=code)
            if target.is_valid():
                user = models.User.objects.get(email=target.email)
                findpw_form = FindPWForm()
                return render(request, "account/pwfind.html", locals())
            else:
                target.delete()
                return redirect("/login/")
        except ObjectDoesNotExist:
            print("AAA")
            return redirect("/login/")