from django.http import HttpResponse
from django.shortcuts import render
from .forms import OrderForm
from .models import Curry, Order
from .domains import OrderDomain
from .exceptions import FormError


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def item_list(request):
    order_list = Order.list()
    curry_list = Curry.list()
    if request.method == 'GET':
        return render(
            request,
            'item_list.html',
            {'form': OrderForm(), 'order_list': order_list, 'curry_list': curry_list}
        )
    else:
        try:
            OrderDomain.post_order(request.POST)
        except FormError as e:
            return render(
                request,
                'item_list.html',
                {'form': e.form, 'order_list': order_list, 'curry_list': curry_list}
            )
        return render(
            request,
            'item_list.html',
            {'form': OrderForm(), 'order_list': order_list, 'curry_list': curry_list}
        )


def order_list(request):
    return render(request, 'order_list.html')
