from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def addcomment(request):
    return HttpResponse("OK")

def rmcomment(request, comment_id):
    return HttpResponse("OK")