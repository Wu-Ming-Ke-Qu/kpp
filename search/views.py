from django.http.response import HttpResponse
from django.shortcuts import render
from course.models import Course
from search.forms import SearchForm, SmallSearchForm
from account.models import User

# Create your views here.
def index(request):
    search_school_id = None
    if request.session.get("is_login", None):
        search_school_id = User.objects.get(pk=request.session['user_id']).school

    search_form = SearchForm(initial={'school': search_school_id})
    small_search_form = SmallSearchForm(initial={'school': search_school_id})

    if request.method == "GET":
        course_name = str(request.GET.get('course'))
        course_list = list(Course.objects.filter(school=str(request.GET.get('school')), 
                                                 course_name__icontains=str(request.GET.get('course'))))
        if course_list == []:
            return render(request, "search/search-noresult.html", locals())
        length = len(course_list)
        return render(request, "search/search-result.html", locals())
    return HttpResponse("OK")