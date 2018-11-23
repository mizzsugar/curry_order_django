from typing import (
    Iterable,
)

from django import forms

from .models import Curry


def generate_curry_choice() -> Iterable[str]:
    return ((curry.id, curry.name) for curry in Curry.objects.all())


class OrderForm(forms.Form):
    user_name = forms.CharField(label='名前', max_length=20)
    curry = forms.ChoiceField(
        label='カレー',
        choices=generate_curry_choice,
        widget=forms.RadioSelect
    )
