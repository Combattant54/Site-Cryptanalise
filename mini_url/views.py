from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from .models import MiniURL
from .forms import AutoMiniURLForm
import random, string

# Create your views here.
def redirect_short(request, url_code:str):
    link = get_object_or_404(MiniURL, url_code = url_code)
    link.access_amount += 1
    link.save()
    return redirect(link.long_url, permanent=True)

def generate_code(letters_number=10):
    charset = string.ascii_letters + string.digits
    random_chars = [random.choice(charset) for _ in range(letters_number)]
    return "".join(random_chars)    

def get_url_form(request):
    url_saved = False
    if request.method == "POST":
        form = AutoMiniURLForm(request.POST)
        
        if form.is_valid():
            code = generate_code()
            while MiniURL.objects.filter(url_code=code).first() is not None:
                code = generate_code()
            
            url_object:MiniURL = form.save(commit=False)
            url_object.url_code = code
            url_object.save()

            url_saved = True
    else: 
        form = AutoMiniURLForm()
    
    return render(request, "mini_url/create_url.html", locals())

def show_redirects(request: HttpRequest):
    links = [(l, request.build_absolute_uri(l.get_absolute_url())) for l in MiniURL.objects.order_by("-access_amount").all()]
    print(links)
    return render(request, "mini_url/show_redirects.html", locals())