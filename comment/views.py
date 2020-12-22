from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .wordcloud_cn import word_cloud
from .models import Comment
from course.models import Course
from account.models import User
from .sensitivity import check_sensitivity
# Create your views here.
def addcomment(request, course_id):
    if not request.session.get('is_login', None):
        return redirect("/login/")

    if request.method == "POST":
        content = request.POST['content']
        if check_sensitivity(content):
            return redirect("/course/" + str(course_id))
        try:
            course = Course.objects.get(pk=course_id)
            user = User.objects.get(pk=request.session['user_id'])
            Comment.objects.create(course=course, user=user, content=content, zan=0, cai=0)
            comment_list = []
            for comment in course.comment_set.all():
                comment_list.append(str(comment.content))
            try:
                word_cloud("static/img/wordcloud/" + str(course_id) + ".png", *comment_list)
            except Exception:
                pass
            return redirect("/course/" + str(course_id))
        except ObjectDoesNotExist:
            return redirect("/course/" + str(course_id))
    
    return redirect("/course/" + str(course_id))

def rmcomment(request, comment_id):
    Comment.objects.get(pk=comment_id).delete()
    return HttpResponse("OK")