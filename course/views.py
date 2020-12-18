from school.models import Department, Teacher
from django.shortcuts import render, redirect
from .forms import CourseForm
from .models import Course, CourseTeacher
from search.forms import SearchForm, SmallSearchForm
# Create your views here.
def addcourse(request):
    if not request.session.get('is_login', None): # 必须登录，否则重定向
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
            return redirect("/course/" + str(course.id))
            
        return render(request, 'course/addcourse.html', locals())
    course_form = CourseForm()
    return render(request, 'course/addcourse.html', locals())

def courseinfo(request, course_id):
    search_form = SearchForm()
    small_search_form = SmallSearchForm()

    course = Course.objects.get(pk=course_id)
    teacher_name = ""
    for teacher in course.teachers.all():
        teacher_name += teacher.teacher_name
    comment = {"islike": True}
    return render(request, 'course/course.html', locals())

def changecourseinfo(request):
    search_form = SearchForm()
    small_search_form = SmallSearchForm()
    return render(request, 'course/changecourseinfo.html', locals())