from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Vote
from account.models import User
from comment.models import Comment

# Create your views here.
def like(request, comment_id):
    if not request.session.get("is_login", None):
        return ('/login/')

    user = User.objects.get(pk = request.session['user_id'])
    comment = Comment.objects.get(pk = comment_id)
    try:
        Vote.objects.get(user=user, comment=comment)
        return HttpResponse("Failed")
    except ObjectDoesNotExist:
        Vote.objects.create(user=user, comment=comment, attr="A")
    return HttpResponse("OK")

def dislike(request, comment_id):
    if not request.session.get("is_login", None):
        return ('/login/')

    user = User.objects.get(pk = request.session['user_id'])
    comment = Comment.objects.get(pk = comment_id)
    try:
        Vote.objects.get(user=user, comment=comment)
        return HttpResponse("Failed")
    except ObjectDoesNotExist:
        Vote.objects.create(user=user, comment=comment, attr="D")
    return HttpResponse("OK")

def clear(request, comment_id):
    if not request.session.get("is_login", None):
        return ('/login/')

    user = User.objects.get(pk = request.session['user_id'])
    comment = Comment.objects.get(pk = comment_id)
    try:
        Vote.objects.get(user=user, comment=comment).delete()
        return HttpResponse("OK")
    except ObjectDoesNotExist:
        return HttpResponse("Failed")