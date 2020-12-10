from django.shortcuts import render

# Create your views here.
def addcourse(request):
    return render(request, 'course/addcourse.html')

def courseinfo(request, course_id):
    if request.session.get('is_login', None):
        return render(request, 'course/course-logged.html')
    else:
        return render(request, 'course/course-not-logged.html')

def changecourseinfo(request):
    return render(request, 'course/changecourseinfo.html')