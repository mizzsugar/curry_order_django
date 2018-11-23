from django.http import HttpResponse
from django.shortcuts import render
from .forms import OrderForm
from .models import Order
from .domains import OrderDomain


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def item_list(request):
    list = Order.list()
    if request.method == 'GET':
        return render(
            request,
            'item_list.html',
            {'form': OrderForm(), 'order_list': list}
        )
    else:
        OrderDomain.post_order(request.POST)
        return render(
            request,
            'item_list.html',
            {'form': OrderForm(), 'order_list': list}
        )


def order_list(request):
    return render(request, 'order_list.html')
