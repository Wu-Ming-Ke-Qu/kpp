from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .wordcloud_cn import word_cloud
# Create your views here.
def addcomment(request):
    word_cloud("static/img/wordcloud/1.png", "你好你好你好你好你好再见再见再见", "你好")
    return HttpResponse("OK")

def rmcomment(request, comment_id):
    return HttpResponse("OK")