from django.shortcuts import render
from .forms import CourseForm
from search.forms import SearchForm, SmallSearchForm
# Create your views here.
def addcourse(request):
    course_form = CourseForm()
    search_form = SearchForm()
    small_search_form = SmallSearchForm()
    return render(request, 'course/addcourse.html', locals())

def courseinfo(request, course_id):
    search_form = SearchForm()
    small_search_form = SmallSearchForm()
    return render(request, 'course/course.html')

def changecourseinfo(request):
    search_form = SearchForm()
    small_search_form = SmallSearchForm()
    return render(request, 'course/changecourseinfo.html')