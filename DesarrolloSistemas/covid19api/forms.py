from django import forms
from .models import User

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'address', 'country']

# class UserForm(forms.Form):
#     fname = forms.CharField(max_length=20, required=False)
#     lname = forms.CharField(max_length=20, required=False)
#     address = forms.CharField(max_length=20, required=False)
#     country = forms.CharField(max_length=15, required=False)
#     password = forms.CharField(widget=forms.PasswordInput, required=False)