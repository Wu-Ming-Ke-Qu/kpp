from account.models import User
from django.core.exceptions import ObjectDoesNotExist
from school.models import Department, Teacher
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CourseForm, ChangeCourseForm
from .models import Course, CourseTeacher
from search.forms import SearchForm, SmallSearchForm
from vote.models import Vote
from comment.models import Comment
from comment.wordcloud_cn import word_cloud
# Create your views here.

def get_user_comment_like(user, comment):
    try:
        vote = Vote.objects.get(user=user, comment=comment)
        if vote.attr == "A":
            return 1
        else:
            return -1
    except ObjectDoesNotExist:
        return 0

def addcourse(request):
    search_school_id = None
    if not request.session.get('is_login', None): # 必须登录，否则重定向
        return redirect('/login/')
    else:
        search_school_id = User.objects.get(pk=request.session['user_id']).school

    search_form = SearchForm(initial={'school': search_school_id})
    small_search_form = SmallSearchForm(initial={'school': search_school_id})

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
            
            same_course_id = Course.objects.filter(course_id = course_id, school = school)
            if same_course_id:
                message = "存在课程号相同的课程！"
                return render(request, 'course/addcourse.html', locals())

            same_department = Department.objects.filter(department_name = department)
            if same_department:
                department = same_department[0]
            else:
                department = Department.objects.create(department_name = department, school = school)
            
            same_teacher = Teacher.objects.filter(teacher_name = teacher, department = department)
            if same_teacher:
                teacher = same_teacher[0]
            else:
                teacher = Teacher.objects.create(teacher_name = teacher, department = department)
            
            if course_id == '':
                course = Course.objects.create(course_name=course_name, school=school, 
                                               department=department,
                                               credit=credit, hour=hour,
                                               pre_course=pre_course)
            else:
                course = Course.objects.create(course_name=course_name, course_id=course_id,
                                               school=school, department=department,
                                               credit=credit, hour=hour,
                                               pre_course=pre_course)
            CourseTeacher.objects.create(course = course, teacher = teacher)
            try:
                word_cloud("static/img/wordcloud/" + str(course.id) + ".png", course_name)
            except Exception:
                pass
            return redirect("/course/" + str(course.id))
            
        return render(request, 'course/addcourse.html', locals())
    course_form = CourseForm()
    return render(request, 'course/addcourse.html', locals())

def courseinfo(request, course_id):
    search_school_id = None
    if request.session.get("is_login", None):
        search_school_id = User.objects.get(pk=request.session['user_id']).school

    search_form = SearchForm(initial={'school': search_school_id})
    small_search_form = SmallSearchForm(initial={'school': search_school_id})

    course = Course.objects.get(pk=course_id)
    user = None
    if request.session.get('is_login', None):
        user = User.objects.get(pk=request.session['user_id'])
    teacher_name = ""
    for teacher in course.teachers.all():
        teacher_name += teacher.teacher_name + " "
    new_comments = []
    for comment in course.comment_set.all()[:3]:
        if comment.is_recent():
            new_comments.append({
                "id": comment.id,
                "content": comment.content, 
                "user": comment.user,
                "like": comment.approve_count(),
                "dislike": comment.disapprove_count(),
                "c_time": comment.c_time,
                "is_folded": comment.is_folded(),
                "islike": True if get_user_comment_like(user, comment) == 1 else False,
                "isunlike": True if get_user_comment_like(user, comment) == -1 else False
            })
    all_comments = []
    for comment in course.comment_set.all():
        all_comments.append({"id": comment.id,
                             "content": comment.content, 
                             "user": comment.user,
                             "like": comment.approve_count(),
                             "dislike": comment.disapprove_count(),
                             "c_time": comment.c_time,
                             "is_folded": comment.is_folded(),
                             "islike": True if get_user_comment_like(user, comment) == 1 else False,
                             "isunlike": True if get_user_comment_like(user, comment) == -1 else False})
    all_number = len(all_comments)
    if all_number != 0 and len(new_comments) == 0:
        new_comments.append(all_comments[0])
    new_number = len(new_comments)

    return render(request, 'course/course.html', locals())

def changecourseinfo(request, course_id):
    search_school_id = None
    if not request.session.get('is_login', None):
        return redirect('/login/')
    else:
        search_school_id = User.objects.get(pk=request.session['user_id']).school

    search_form = SearchForm(initial={'school': search_school_id})
    small_search_form = SmallSearchForm(initial={'school': search_school_id})

    if request.method == "POST":
        change_course_form = ChangeCourseForm(request.POST)
        if change_course_form.is_valid():
            credit = change_course_form.cleaned_data["credit"]
            hour = change_course_form.cleaned_data["hour"]
            pre_course = change_course_form.cleaned_data["pre_course"]
            if credit == "" or hour == "":
                messages.add_message(request, messages.WARNING, "请检查填写的内容！")
                return redirect('/course/changecourseinfo/' + str(course_id))
            try:
                credit = float(credit)
                hour = float(hour)
            except Exception:
                messages.add_message(request, messages.WARNING, "请填写正确的学分和学时！")
                return redirect('/course/changecourseinfo/' + str(course_id))
            course = Course.objects.get(pk=course_id)
            course.credit = credit
            course.hour = hour
            course.pre_course = pre_course
            course.save()
            return redirect('/course/' + str(course_id))
        else:
            messages.add_message(request, messages.WARNING, "请检查填写的内容！")
            return redirect('/course/changecourseinfo/' + str(course_id))

    course = Course.objects.get(pk=course_id)
    teacher_name = ""
    for teacher in course.teachers.all():
        teacher_name += teacher.teacher_name + " "
    change_course_form = ChangeCourseForm()
    return render(request, 'course/changecourseinfo.html', locals())