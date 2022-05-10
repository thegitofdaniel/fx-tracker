from django.http import HttpResponse	
from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
	#print(args, kwargs)
	#print(request.user)
	#return HttpResponse("<h1>Hello, World</h1>")
    return render(request, "home.html", {})

def brl_view(request, *args, **kwargs):
	return render(request, "brl.html", {})

def eur_view(request, *args, **kwargs):
	return render(request, "eur.html", {})

def about_view(request, *args, **kwargs):
	return render(request, "about.html", {})