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
    Decaf = forms.ChoiceField(label='카페인/디카페인', widget=forms.RadioSelect, choices=Caffeine_Choice)

    CoffeeType_Choice = [
        ('0', '싱글 오리진'),
        ('1', '블렌드'),
    ]
    CoffeeType = forms.ChoiceField(label='커피 타입', widget=forms.RadioSelect, choices=CoffeeType_Choice)

    NOTE_CHOICES = (
        ("꽃", "꽃"),
        ("과일", "과일"),
        ("초콜릿", "초콜릿"),
        ("향료", "향료"),
        ("달콤함", "달콤함"),
        ("고소함", "고소함"),
        ("허브", "허브"),
    )
    CupNotes = forms.MultipleChoiceField(label='커피 향 노트 (중복 선택 가능)', choices=NOTE_CHOICES, widget=forms.CheckboxSelectMultiple)

    Sourness = forms.IntegerField(label='신맛',
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '5', 'value': '3'}))

    Sweetness = forms.IntegerField(label='단맛',
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '5', 'value': '3'}))

    Bitterness = forms.IntegerField(label='쓴맛',
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '5', 'value': '3'}))

    Body = forms.IntegerField(label='바디감',
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '5', 'value': '3'}))
