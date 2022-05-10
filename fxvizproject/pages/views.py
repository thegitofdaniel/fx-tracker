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
	my_context = {
					"my_text": "This is about us."
					,"my_number":123
					,"this_is_true":True
					,"my_list":[1,2,3,4,5,6,7,9]
					,"my_html":"<h1>This is html.</h1>"
					}
	return render(request, "about.html", my_context)