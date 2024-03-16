# forms.py
from django import forms
from datetime import datetime    

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=50, required=True)
    subject = forms.CharField(max_length=30, required=True)
    message = forms.CharField(max_length=255, required=True)
    #time = forms.DateTimeField(default=datetime.now(), blank=True)