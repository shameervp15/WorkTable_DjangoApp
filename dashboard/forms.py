from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *

class NotesForms(forms.ModelForm):
    class Meta:
        model = NotesModel
        fields = ['title', 'description']

class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworksForms(forms.ModelForm):
    class Meta:
        model = HomeworkModels
        widgets = {'due' : DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']

class YoutubeForms(forms.Form):
    text = forms.CharField(max_length=100,label="Search here:")

class TodoForms(forms.Form):
    class Meta:
        model = TodoModel
        fields = ['title', 'is_finished']

class BookForms(forms.Form):
    text = forms.CharField(max_length=100,label="Search Here: ")

class DictionaryForms(forms.Form):
    text = forms.CharField(max_length=100,label="Search Here: ")

class WikiForms(forms.Form):
    text = forms.CharField(max_length=100, label="Search Here:")

class ConversionForms(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionLengthForms(forms.Form):
    Choices = [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type':'number','placeholder': 'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label = '',widget=forms.Select(choices=Choices)
    )
    measure2 = forms.CharField(
        label = '',widget=forms.Select(choices=Choices)
    )

class ConversionMassForms(forms.Form):
    Choices = [('pound','Pound'),('kilograms','Kilograms')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type':'number','placeholder': 'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label = '',widget=forms.Select(choices=Choices)
    )
    measure2 = forms.CharField(
        label = '',widget=forms.Select(choices=Choices)
    )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']