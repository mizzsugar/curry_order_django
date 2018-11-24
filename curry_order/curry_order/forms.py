from typing import (
    Iterable,
)

from django import forms

from .models import Curry


def generate_curry_choice() -> Iterable[str]:
    return ((curry.id, curry.name) for curry in Curry.objects.all())

class ImageSelect(forms.widgets.RadioSelect):
    template_name = 'templates/widgets/curry_radio.html' # 自作
    option_template_name = 'templates/widgets/curry_radio_option.html'


class OrderForm(forms.Form):
    user_name = forms.CharField(label='名前', max_length=20)
    curry = forms.ChoiceField(
        label='カレー',
        choices=generate_curry_choice,
        widget=ImageSelect
    )


