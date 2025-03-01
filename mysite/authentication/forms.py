from cProfile import label
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.core.exceptions import ValidationError
from numpy import require

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(max_length=20,label="USERNAME ", required = True,  widget=forms.TextInput(attrs={'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}))
	email = forms.EmailField(label="EMAIL", required=True,widget=forms.TextInput(attrs={'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}))
	first_name = forms.CharField(max_length = 20,label="FIRST NAME",widget=forms.TextInput(attrs={'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}))
	last_name = forms.CharField(max_length = 20,label="SECOND NAME",widget=forms.TextInput(attrs={'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}))
	password1 = forms.CharField(label="ENTER PASSWORD", widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}))
	password2 = forms.CharField(label="CONFIRM PASSWORD", widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6 mb-5'}))

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

class ProfileEditForm(UserChangeForm):
    # User fields
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Profile fields
    profileBg = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about yourself...'}), required=False)
    location = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Location'}), required=False)
    occupation = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Occupation'}), required=False)
    indsutry = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Industry'}), required=False)
    profileImage = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), required=False)
    twitter_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False, initial="https://x.com/")
    instagram_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False, initial="https://instagram.com/")
    youtube_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False, initial="https://youtube.com/")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'] = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)
        self.fields['profileImage'] = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), required=False)
        self.fields['twitter_link'] = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
        self.fields['instagram_link'] = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
        self.fields['youtube_link'] = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
        
    

    
