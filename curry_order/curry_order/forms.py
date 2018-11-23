from typing import (
    Iterable,
)

from django import forms

from .models import Curry, Order


def generate_curry_choice() -> Iterable[str]:
    return ((str(curry.id), curry.name) for curry in Curry.objects.all())


class OrderForm(forms.Form):
    curry = forms.ChoiceField(label='カレー', choices=generate_curry_choice, widget=forms.RadioSelect)

