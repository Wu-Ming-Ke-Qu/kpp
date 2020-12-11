from django.shortcuts import render

# Create your views here.
def addcourse(request):
    return render(request, 'course/addcourse.html')

def courseinfo(request, course_id):
    return render(request, 'course/course.html')

def changecourseinfo(request):
    return render(request, 'course/changecourseinfo.html')