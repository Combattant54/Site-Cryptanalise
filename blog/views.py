from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, Http404
from django.http.request import HttpRequest

from django.urls import reverse

import datetime, pytz

from .models import Categorie, Article, Profile, Tokens
from .forms import ContactForm, ConnexionForm, CreateUserForm
from .utils import sendmail, gmail_sendmail, base36encode, base36decode

text = "<h1 style='center'>Page de maintenance</h1>\n<h3>Le site est actuellement en maintenance, merce de votre compréhension.</h3>"
resp = HttpResponse(text)

# Create your views here.
def home(request):
    return render(request, "blog/accueil.html", {"articles": Article.objects.order_by("-date_creation").all()})

def show_recent_articles(request):
    return redirect(home, permanent=True)
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
        form = ConnexionForm()
    
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


def create_profile(request: HttpRequest):
    user_created = False
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["pass1"]
                email = form.cleaned_data["email"]
                user = User.objects.create_user(username=username, password=password, email=email)
                
                profile = Profile()
                profile.user = user
                profile.self_presentation = ""
                profile.is_active = False
                profile.save()
                
                userid_b36 = base36encode(user.id)
                token = Tokens()
                token.url = "/"
                token.user = user
                token.save()
                print(userid_b36, token.token)
                url = reverse("confirm_user_creation", args=(userid_b36, token.token))
                token.url = url
                token.save()
                
                full_url = request.build_absolute_uri(url)
                print(full_url)
                subject = "Création de votre compte Cryptanalitica"
                
                message = f"""
                    <h1> Création de votre compte sur {request.get_host()} </h1>
                    
                    <h3>Clickez sur le lien pour accéder à votre compte</h1>
                    <h3>(si vous n'êtes pas {username} et vous n'avez pas demander ce mail, merci d'ignorer ce mail)</h3>
                    
                    <a href="{full_url}">{full_url}</a>
                    
                    Merci, le staff de cryptanalitica
                """
                
                print(sendmail(subject, message, email))
                return redirect(waiting_account_confirmation, permanent=True)
            except Exception as e:
                print(e)
                user.delete()
                profile.delete()
                token.delete()
                raise e
    else:
        form = CreateUserForm()
    return render(request, "create_account.html", locals())

def waiting_account_confirmation(request, next="private_profile"):
    return render(request, "waiting_account_creation_confirmation.html", locals())

def get_articles_from_category(request, id, slug=None):
    if slug is None or slug == "":
        cat = get_object_or_404(Categorie, id=id)
        if cat.slug is None:
            cat.save()
        return redirect(get_articles_from_category, id, cat.slug, permanent=True)
    
    category = get_object_or_404(Categorie, id=id, slug=slug)
    articles = category.articles.order_by("-date_creation")
    
    return render(request, "blog/articles_by_category.html", locals())

def confirm_user_creation(request: HttpRequest, userid_b36, token):
    id = base36decode(userid_b36)
    user = User.objects.get(id=id)
    token = Tokens.objects.filter(url=reverse("confirm_user_creation", args=(userid_b36, token)), user=user, token=token).first()
    if datetime.datetime.now(tz=pytz.timezone("Europe/Paris")) < token.expiration_date:
        profile = Profile.objects.get(user=user)
        profile.is_active = True
        profile.save()
        
        token.delete()
        
        if request.user.is_authenticated:
            logout(request)
        
        return redirect("connexion", permanent=True)

    return redirect("create_user_profile")