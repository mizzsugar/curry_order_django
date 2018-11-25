from typing import (
    Iterable,
    Tuple,
)

from django import forms

from .models import Curry


class OrderEntryForm(forms.Form):
    group = forms.CharField(label='団体名', max_length=20)


def generate_curry_choice() -> Iterable[Tuple[int, str]]:
    class MyLabel:
        def __init__(self, name: str, image: str, price: int) -> None:
            self.name = name
            self.image = image
            self.price = price

        def __str__(self):
            return self.name

    return (
        (curry.id, MyLabel(curry.name, curry.image, curry.price))
        for curry in Curry.objects.all()
    )


class ImageSelect(forms.widgets.RadioSelect):
    template_name = 'widgets/curry_radio.html'
    option_template_name = 'widgets/curry_radio_option.html'


class OrderForm(forms.Form):
    user_name = forms.CharField(label='名前', max_length=20)
    curry = forms.ChoiceField(
        label='カレー',
        choices=generate_curry_choice,
        widget=ImageSelect
    )
