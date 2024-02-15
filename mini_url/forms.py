from django import forms
from .models import MiniURL

class AutoMiniURLForm(forms.ModelForm):
    class Meta:
        model = MiniURL
        fields = ("long_url", "creator")


