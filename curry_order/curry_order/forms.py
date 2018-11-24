from typing import (
    Iterable,
    Tuple,
NamedTuple,
)

from django import forms

from .models import Curry


def generate_curry_choice() -> Iterable[Tuple[int, str]]:
    class MyLabel:
        def __init__(self, name: str, image: str, price: int) -> None:
            self.name = name
            self.image = image
            self.price = price

    return (
        (curry.id, MyLabel(curry.name, curry.image, curry.price))#(curry.name, curry.image))
        for curry in Curry.objects.all()
    )

class ImageSelect(forms.widgets.RadioSelect):
    # template_name = 'templates/widgets/curry_radio.html' # 自作
    # option_template_name = 'templates/widgets/curry_radio_option.html'
    template_name = 'widgets/curry_radio.html' # 自作
    option_template_name = 'widgets/curry_radio_option.html'


class OrderForm(forms.Form):
    user_name = forms.CharField(label='名前', max_length=20)
    curry = forms.ChoiceField(
        label='カレー',
        choices=generate_curry_choice,
        widget=ImageSelect
    )
