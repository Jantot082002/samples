# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your old password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your new password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your new password'}))

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']