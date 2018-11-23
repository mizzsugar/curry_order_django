from django.http import HttpResponse
from django.shortcuts import render
from .forms import OrderForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def item_list(request):
    form = OrderForm()
    return render(request, 'item_list.html', {'form': form})

def order_list(request):
    return render(request, 'order_list.html')
