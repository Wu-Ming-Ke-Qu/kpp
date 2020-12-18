from django.shortcuts import render, redirect
from .forms import CourseForm
from .models import Course
from search.forms import SearchForm, SmallSearchForm
# Create your views here.
def addcourse(request):
    if not request.session.get('is_login', None): # 本身就没有登录，无需登出
        return redirect('/login/')

    search_form = SearchForm()
    small_search_form = SmallSearchForm()

    if request.method == "POST":
        course_form=CourseForm(request.POST)
        message = "请检查填写的内容！"
        if course_form.is_valid():
            course_name=course_form.cleaned_data['course_name']
            course_id=course_form.cleaned_data['course_id']
            school=course_form.cleaned_data['school']
            department=course_form.cleaned_data['department']
            teacher=course_form.cleaned_data['teacher']
            credit=course_form.cleaned_data['credit']
            hour=course_form.cleaned_data['hour']
            pre_course=course_form.cleaned_data['pre_course']
            
            

        return render(request, 'course/addcourse.html', locals())
    course_form = CourseForm()
    return render(request, 'course/addcourse.html', locals())

def courseinfo(request, course_id):
    if not request.session.get('is_login', None):
        return redirect("/login/")

    search_form = SearchForm()
    small_search_form = SmallSearchForm()

    course = Course.objects.get(pk=course_id)
    return render(request, 'course/course.html', locals())

def changecourseinfo(request):
    search_form = SearchForm()
    small_search_form = SmallSearchForm()
    return render(request, 'course/changecourseinfo.html', locals())