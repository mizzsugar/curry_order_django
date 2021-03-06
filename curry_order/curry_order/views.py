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
        return HttpResponseRedirect('/url_does_not_exist')
    if request.method == 'POST':
        try:
            OrderDomain.post_order(request.POST, group_uuid)
        except DoesNotExistError:
            return HttpResponseRedirect('/url_does_not_exist')
        except FormError as e:
            order_list = OrderDomain.get_order_by_group_uuid(group_uuid=group_uuid)
            order_sum = OrderDomain.get_order_sum(group_uuid)
            return render(
                request,
                'order_form.html',
                {'form': e.form,
                 'order_list': order_list,
                 'group': group,
                 'order_sum': order_sum
                 }
            )
        order_list = OrderDomain.get_order_by_group_uuid(group_uuid=group_uuid)
        order_sum = OrderDomain.get_order_sum(group_uuid)
        return render(
            request,
            'order_form.html',
            {'form': OrderForm(),
             'order_list': order_list,
             'group': group,
             'order_sum': order_sum
             }
        )
    else:
        order_list = OrderDomain.get_order_by_group_uuid(group_uuid=group_uuid)
        order_sum = OrderDomain.get_order_sum(group_uuid)
        return render(
            request,
            'order_form.html',
            {'form': OrderForm(),
             'order_list': order_list,
             'group': group, 'order_sum': order_sum,
             'order_sum': order_sum
            }
        )


def order_update_form(request, group_uuid, order_id):
    try:
        group = OrderEntryDomain.get_by_uuid(url_uuid=group_uuid)
    except DoesNotExistError:
        return HttpResponseRedirect('/url_does_not_exist')
    order_list = OrderDomain.get_order_by_group_uuid(group_uuid=group_uuid)
    order_sum = OrderDomain.get_order_sum(group_uuid)
    try:
        update_order = OrderDomain.get_by_orderid(id=order_id)
    except DoesNotExistError:
        return HttpResponseRedirect('/url_does_not_exist')
    if request.method == 'GET':
        form = OrderForm(
            {'user_name': update_order.user_name,
             'curry': update_order.curry.id
             }
        )
        return render(
            request,
            'order_update_form.html',
            {'form': form,
             'order_list': order_list,
             'group': group,
             'update_order': update_order,
             'order_sum': order_sum
             }
        )
    else:
        try:
            update_order = OrderDomain.update_order(request.POST, update_order)
        except FormError as e:
            return render(
                request,
                'order_update_form.html',
                {'form': e.form,
                 'order_list': order_list,
                 'group': group,
                 'update_order': update_order,
                 'order_sum': order_sum
                 }
            )
        return HttpResponseRedirect(
            reverse('order-form', args=(group.url_uuid,))
        )


def order_delete_form(request, group_uuid, order_id):
    try:
        group = OrderEntryDomain.get_by_uuid(url_uuid=group_uuid)
    except DoesNotExistError:
        return HttpResponseRedirect('/url_does_not_exist')  # 404
    try:
        OrderDomain.delete_order(order_id)
    except DoesNotExistError:
        return HttpResponseRedirect(
            reverse('order-form', args=(group.url_uuid,))  # 404
        )
    return HttpResponseRedirect(
        reverse('order-form', args=(group.url_uuid,))
    )


def url_does_not_exist(request):
    return render(request, '404.html')
