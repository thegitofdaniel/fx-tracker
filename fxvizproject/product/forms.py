from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
	title			= forms.CharField(
									label="My title"
									,widget=forms.TextInput(
										attrs={
												"placeholder":"your title"
												}
										)
									)
	email 			= forms.EmailField()
	description		= forms.CharField(
									required=False
									,widget=forms.Textarea(
										attrs={
												"placeholder":"your title"
												,"class":"new-class-name two"
												,"rows":10
												,"cols":20
												,"id":"my-id-for-textarea"
												}
										)
									)
	price			= forms.DecimalField(initial=100.00)
	
	class Meta:
		model = Product
		fields = [
					"title"
					,"description"
					,"price"
					]

	def clean_title(self, *args, **kwargs):
		title = self.cleaned_data.get("title")
		if not "CFE" in title:
			raise forms.ValidationError("This is not a  valid title.")
		else:
			return title

	def clean_email(self, *args, **kwargs):
		email = self.cleaned_data.get("email")
		if not email.endswith("edu"):
			raise forms.ValidationError("This is not a  valid email.")
		else:
			return title

class RawProductForm(forms.Form):
	title			= forms.CharField(
										label=""
										,widget=forms.TextInput(
											attrs={
													"placeholder":"your title"
													}
											)
										)
	description		= forms.CharField(
										required=False
										,widget=forms.Textarea(
											attrs={
													"placeholder":"your title"
													,"class":"new-class-name two"
													,"rows":10
													,"cols":20
													,"id":"my-id-for-textarea"
													}
											)
										)
	price			= forms.DecimalField(initial=100.00)