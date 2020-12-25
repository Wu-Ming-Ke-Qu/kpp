from django.http.response import HttpResponse
from django.shortcuts import render
from course.models import Course
from search.forms import SearchForm, SmallSearchForm
from account.models import User
from copy import deepcopy

# Create your views here.
def index(request):
    search_school_id = None
    if request.session.get("is_login", None):
        search_school_id = User.objects.get(pk=request.session['user_id']).school

    search_form = SearchForm(initial={'school': search_school_id})
    small_search_form = SmallSearchForm(initial={'school': search_school_id})

    if request.method == "GET":
        course_name = request.GET.get('course')
        if not course_name:
            course_list = list(Course.objects.filter(school=str(request.GET.get('school'))))
        else:
            course_list = list(Course.objects.filter(school=str(request.GET.get('school')), 
                                                 course_name__icontains=str(request.GET.get('course'))))
        if course_list == []:
            return render(request, "search/search-noresult.html", locals())
        length = len(course_list)
        new_course_list = []
        for course in course_list:
            teacher_name = ""
            for teacher in course.teachers.all():
                teacher_name += teacher.teacher_name + " "
            new_course_list.append({
                "id": course.id,
                "course_name": course.course_name,
                "school": course.school.school_name,
                "comment_count": course.comment_count(),
                "teacher_name": deepcopy(teacher_name)})
        course_list = new_course_list
        return render(request, "search/search-result.html", locals())
    return HttpResponse("OK")