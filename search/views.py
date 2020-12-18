from django.http.response import HttpResponse
from django.shortcuts import render
from course.models import Course
from search.forms import SearchForm, SmallSearchForm

# Create your views here.
def index(request):
    if request.method == "GET":
        course_list = list(Course.objects.filter(school=str(request.GET.get('school')), 
                                                 course_name__icontains=str(request.GET.get('course'))))
        if course_list == []:
            search_form = SearchForm()
            small_search_form = SmallSearchForm()
            return render(request, "search/search-noresult.html", locals())
        search_form = SearchForm()
        small_search_form = SmallSearchForm()
        return render(request, "search/search-result.html", locals())
    return HttpResponse("OK")