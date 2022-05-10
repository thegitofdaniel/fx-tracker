from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

# Create your views here.
from .models import Product
from .forms import ProductForm, RawProductForm


################################################

"""
def product_create_view(request):
	# pure html form
	print(request.POST)
	my_new_title = request.POST.get("title")
	print(my_new_title)
	context = {}
	return render(request, "products/product_create.html", context)

def product_create_view(request):
	my_form = RawProductForm()
	# pure django form
	if request.method == "POST":
		my_form = RawProductForm(request.POST)
		if my_form.is_valid():
			print(my_form.cleaned_data)
			Product.objects.create(**my_form.cleaned_data)
			my_form = RawProductForm()
		else:
			print(my_form.errors)
"""

def product_create_view(request):
	form = ProductForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = ProductForm() #re-render to clean form after submit
	context = {"form": form}
	return render(request, "products/product_create.html", context)
			
	context = {"form": my_form}
	return render(request, "products/product_create.html", context)

def product_update_view(request, id):
	obj = get_object_or_404(Product, id=id)
	form = ProductForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
	context = {"form": form}
	return render(request, "products/product_create.html", context)

def product_delete_view(request, id):
	obj = get_object_or_404(Product, id=id)
	if request.method == "POST":
		# confirming delete
		obj.delete()
		return redirect("../")
	context = {"object": obj}
	return render(request, "products/product_delete.html", context)

################################################

def product_detail_view(request, id=1):
	obj = Product.objects.get(id=id)
	context = {"object": obj}
	return render(request, "products/product_detail.html", context)

def dynamic_lookup_view(request, id):
	"""
	try:
		obj = Product.objects.get(id=id)
	except Product.DoesNotExist:
		raise Http404
	"""
	obj = get_object_or_404(Product, id=id)
	context = {"object": obj}
	return render(request, "products/product_detail.html", context)

def product_list_view(request):
	queryset = Product.objects.all() # list of all objects
	context = {"object_list": queryset}
	return render(request, "products/product_list.html", context)

################################################