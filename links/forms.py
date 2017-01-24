from django import forms
from .models import UserProfile, Link

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user", )

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ('submitter', 'score')