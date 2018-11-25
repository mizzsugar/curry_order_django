from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from .forms import OrderEntryForm, OrderForm
from .models import Order
from .domains import GroupEntryDomain, OrderDomain
from .exceptions import FormError


def order_entry(request):
    if request.method == 'GET':
        return render(request, 'order_entry.html', {'form': OrderEntryForm()})
    else:
        try:
            group = GroupEntryDomain.register_group(request.POST)
        except FormError as e:
            return render(request, 'order_entry.html', {'form': e.form})
        return HttpResponseRedirect(reverse('show-group-url', args=(group.url_uuid,)))


def show_group_url(request, group_uuid):
    group = GroupEntryDomain.get_by_uuid(url_uuid=group_uuid)
    print(group_uuid)
    return render(request, 'show_group_url.html', {'group': group})


def item_list(request):
    order_list = Order.list()
    if request.method == 'GET':
        return render(
            request,
            'item_list.html',
            {'form': OrderForm(), 'order_list': order_list}
        )
    else:
        try:
            OrderDomain.post_order(request.POST)
        except FormError as e:
            return render(
                request,
                'item_list.html',
                {'form': e.form, 'order_list': order_list}
            )
        return render(
            request,
            'item_list.html',
            {'form': OrderForm(), 'order_list': order_list}
        )


def order_list(request):
    return render(request, 'order_list.html')
