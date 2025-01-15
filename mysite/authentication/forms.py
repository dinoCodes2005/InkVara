from cProfile import label

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(max_length=20,label="USERNAME ")
	email = forms.EmailField(label="EMAIL")
	first_name = forms.CharField(max_length = 20,label="FIRST NAME")
	last_name = forms.CharField(max_length = 20,label="SECOND NAME")
	password1 = forms.CharField(label="ENTER PASSWORD", widget=forms.PasswordInput())
	password2 = forms.CharField(label="CONFIRM PASSWORD", widget=forms.PasswordInput())

	def clean(self):
		cleaned_data = super().clean()
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2:
			if password1!=password2:
				raise ValidationError("The two password fields must match.")

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name','last_name','password1', 'password2']
