from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from .forms import OrderEntryForm, OrderForm
from .domains import OrderEntryDomain, OrderDomain
from .exceptions import FormError, DoesNotExistError


def order_entry(request):
    if request.method == 'GET':
        return render(request, 'order_entry.html', {'form': OrderEntryForm()})
    else:
        try:
            group = OrderEntryDomain.register_group(request.POST)
        except FormError as e:
            return render(request, 'order_entry.html', {'form': e.form})
        return HttpResponseRedirect(
            reverse('show-group-url', args=(group.url_uuid,))
        )


def show_group_url(request, group_uuid):
    group = OrderEntryDomain.get_by_uuid(url_uuid=group_uuid)
    return render(request, 'show_group_url.html', {'group': group})


def order_form(request, group_uuid):
    try:
        group = OrderEntryDomain.get_by_uuid(url_uuid=group_uuid)
    except DoesNotExistError:
        return HttpResponse('Hello, DoesNotExist')
    order_list = OrderDomain.get_order_by_group_uuid(group_uuid=group_uuid)
    if request.method == 'GET':
        return render(
            request,
            'order_form.html',
            {'form': OrderForm(), 'order_list': order_list, 'group': group}
        )
    else:
        try:
            OrderDomain.post_order(request.POST, group_uuid)
        except DoesNotExistError:
            return HttpResponse('hello, DoesNotExistError')
        except FormError as e:
            return render(
                request,
                'order_form.html',
                {'form': e.form, 'order_list': order_list, 'group': group}
            )
        return render(
            request,
            'order_form.html',
            {'form': OrderForm(), 'order_list': order_list, 'group': group}
        )
