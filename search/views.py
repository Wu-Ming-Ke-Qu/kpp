from django.http.response import HttpResponse
from django.shortcuts import render
from course.models import Course

# Create your views here.
def index(request):
    if request.method == "GET":
        course_list = list(Course.objects.filter(school=str(request.GET.get('school')), 
                                                 course_name__icontains=str(request.GET.get('course'))))
        if course_list == []:
            return render(request, "search/search-noresult.html", locals())
        return render(request, "search/search-result.html", locals())
    return HttpResponse("OK")