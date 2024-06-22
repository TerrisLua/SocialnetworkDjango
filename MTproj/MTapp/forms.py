from django import forms
from .models import *

# I wrote this code
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ("image", "status_update")


class UserSearchForm(forms.Form):
    query = forms.CharField(label="Search for users", max_length=100)


class MediaPostForm(forms.ModelForm):
    class Meta:
        model = MediaPost
        fields = ("media", "text_content")


class UpdateProfileImageForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ["image"]


class UpdateProfileStatusForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ["status_update"]


# end of code I wrote
