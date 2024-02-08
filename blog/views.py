from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect

text = "<h1 style='center'>Page de maintenance</h1>\n<h3>Le site est actuellement en maintenance, merce de votre compréhension.</h3>"
resp = HttpResponse(text)

# Create your views here.
def home(request):
    return resp

def show_recent_articles(request):
    return redirect("https://www.wikipedia.org")

def show_article(request, id:int):
    if id > 100:
        return Http404
    return resp

def search_date_articles(request, year:int, month:int):
    return resp
