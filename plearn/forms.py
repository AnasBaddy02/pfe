from django import forms
from .models import Section

class CreateSection(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', 'content', 'video')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sections name', 'required': 'True'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': "5", 'placeholder': 'Sections content', 'required': 'True'}),
            'video': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL', 'required': 'True'}),
        }

class EditSection(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', 'content', 'video')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sections name'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': "5", 'placeholder': 'Sections content'}),
            'video': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL'}),
        }
