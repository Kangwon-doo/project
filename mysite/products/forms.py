from django import forms
from main.models import test_preference, test_Reviews


class EmailForm(forms.ModelForm):
    # email = forms.EmailField(error_messages={'required':'이메일을 입력해주세요.', 'invalid':'이메일을 올바르게 입력해주세요'})
    class Meta:
        model = test_preference
        fields = ('email',)


class PreferenceForm(forms.Form):
    Caffeine_Choice = [
        ('0', '카페인'),
        ('1', '디카페인'),
    ]
    Decaf = forms.ChoiceField(widget=forms.RadioSelect, choices=Caffeine_Choice)

    CoffeeType_Choice = [
        ('0', '싱글 오리진'),
        ('1', '블렌드'),
    ]
    CoffeeType = forms.ChoiceField(widget=forms.RadioSelect, choices=CoffeeType_Choice)

    NOTE_CHOICES = (
        ("꽃", "꽃"),
        ("과일", "과일"),
        ("초콜릿", "초콜릿"),
        ("향료", "향료"),
        ("달콤함", "달콤함"),
        ("고소함", "고소함"),
        ("허브", "허브"),
    )
    CupNotes = forms.MultipleChoiceField(choices=NOTE_CHOICES, widget=forms.CheckboxSelectMultiple)

    Sourness = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '5', 'value': '3'}))

    Sweetness = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '5', 'value': '3'}))

    Bitterness = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '5', 'value': '3'}))

    Body = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '5', 'value': '3'}))


class PredictionForm(forms.ModelForm):
    class Meta:
        model = test_Reviews
        fields = ('CoffeeID', 'Stars', 'created_date')