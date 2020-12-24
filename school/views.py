from django.http.response import HttpResponse
from django.shortcuts import render
from search.forms import SearchForm, SmallSearchForm
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .forms import AddSchoolFrom
from account.models import User

def send_email(email, school_type, school_name, school_email_addr):
    subject = '课评评请求添加学校'
    text_content = '''尊敬的管理员，\
                      如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''<p>您的网站 课评评 收到了一条请求，请求添加的学校信息如下：</p>
                    <p>学校类型：{}</p>
                    <p>学校全称：{}</p>
                    <p>学校邮箱后缀：{}</p>
                    <p>请认真考虑，在后台添加</p>'''.format(
                        school_type,
                        school_name,
                        school_email_addr)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()
# Create your views here.
def schoolinfo(request):
    return HttpResponse("OK")

def addschool(request):
    search_school_id = None
    if request.session.get("is_login", None):
        search_school_id = User.objects.get(pk=request.session['user_id']).school

    search_form = SearchForm(initial={'school': search_school_id})
    small_search_form = SmallSearchForm(initial={'school': search_school_id})

    if request.method == "POST":
        add_school_form = AddSchoolFrom(request.POST)
        message = "请检查填写的内容！"
        if add_school_form.is_valid():
            school_type = add_school_form.cleaned_data['school_type']
            school_name = add_school_form.cleaned_data['school_name']
            school_email_addr = add_school_form.cleaned_data['school_email_addr']
            send_email("guyi2000@yeah.net" ,school_type, school_name, school_email_addr)
            message = "发送请求成功，我们将会在24小时内处理！"
        return render(request, 'account/addschool.html', locals())

    add_school_form = AddSchoolFrom()
    return render(request, 'account/addschool.html', locals())