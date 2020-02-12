from django import forms
from .models import Snippet
from django_ace import AceWidget

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        widgets = {
            "text": AceWidget(mode='python', theme='twilight',
                              showinvisibles=True, tabsize=4),
        }
        exclude = ()