"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import Camps

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class NewRefugee(forms.Form):
    camp = forms.ModelChoiceField(label="Camp: ",queryset=Camps.objects.all())
    noOfPeople = forms.IntegerField(label='Number of People: ');
    specialNeeds = forms.CharField(label='Special Needs: ')


class ChooseCamp(forms.Form):
    camp = forms.ModelChoiceField(label="Camp: ",queryset=Camps.objects.all())

class AddResources(forms.Form):
    camp = forms.ModelChoiceField(label="Camp: ",queryset=Camps.objects.all())
    resources = forms.CharField(label='Resources: ')

class AllocateResources(forms.Form):
    resources = forms.CharField(label='Resources: ')

