from django.http.response import HttpResponse
from django.shortcuts import render
from search.forms import SearchForm, SmallSearchForm

# Create your views here.
def schoolinfo(request):
    return HttpResponse("OK")

def addschool(request):
    search_form = SearchForm()
    small_search_form = SmallSearchForm()
    
    return render(request, 'account/addschool.html', locals())