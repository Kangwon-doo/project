from django import forms
from main.models import Temp

class TempForm(forms.ModelForm):
    
    
    class Meta:
        model = Temp
        fields = ("Caffeine",)

