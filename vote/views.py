from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def like(request, comment_id):
    return HttpResponse("OK")

def dislike(request, comment_id):
    return HttpResponse("OK")