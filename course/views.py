from django.shortcuts import render
from .forms import CourseForm

# Create your views here.
def addcourse(request):
    course_form = CourseForm()
    return render(request, 'course/addcourse.html', locals())

def courseinfo(request, course_id):
    return render(request, 'course/course.html')

def changecourseinfo(request):
    return render(request, 'course/changecourseinfo.html')