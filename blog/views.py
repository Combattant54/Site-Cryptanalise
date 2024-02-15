from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, Http404
from django.http.request import HttpRequest

from django.urls import reverse

from .models import Categorie, Article, Profile
from .forms import ContactForm, ConnexionForm

text = "<h1 style='center'>Page de maintenance</h1>\n<h3>Le site est actuellement en maintenance, merce de votre compréhension.</h3>"
resp = HttpResponse(text)

# Create your views here.
def home(request):
    return render(request, "blog/accueil.html", {"derniers_articles": Article.objects.all()})

def show_recent_articles(request):
    return redirect("https://www.wikipedia.org")

def redirect_article_with_slug(request, id: int):
    art = get_object_or_404(Article, id=id)
    if art.slug is None:
        art.save()
    return redirect(art.slug)
    return redirect("blog.view.article", id, art.slug)

def show_article(request: HttpRequest, id:int, slug:str=None):
    art = get_object_or_404(Article, id=id, slug=slug)
    return render(request, "blog/article.html", {"article":art})

def search_date_articles(request, year:int, month:int):
    return resp


def contact(request: HttpRequest):
    if request.method == "POST":
        form = ContactForm(request.POST)
        
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            content = form.cleaned_data["content"]
            sender = form.cleaned_data["sender"]
            sendback = form.cleaned_data["sendback"]
            
            
            
            sent = True
    else:
        form = ContactForm()
    
    return render(request, "blog/contact.html", locals())

def connexion(request: HttpRequest):
    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                error = True
    else:
        form = ConnexionForm
    
    return render(request, "login.html", locals())

def deconnexion(request):
    logout(request)
    return redirect(reverse("connexion"))

def see_profile(request:HttpRequest, username):
    if request.user.is_authenticated and request.user.username == username:
        return redirect(reverse("private_profile"), permanent=True)
    
    user = get_object_or_404(User, username=username)
    profile, found = Profile.objects.get_or_create(user=user)
    
    articles = profile.written_articles.all()

    return render(request, "profile.html", locals())
    

@login_required
def see_private_profile(request: HttpRequest):
    profile, found = Profile.objects.get_or_create(user=request.user)
    
    return render(request, "private_profile.html", locals())
