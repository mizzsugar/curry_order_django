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
    order_sum = OrderDomain.get_order_sum(group_uuid)
    if request.method == 'GET':
        return render(
            request,
            'order_form.html',
            {'form': OrderForm(),
             'order_list': order_list,
             'group': group, 'order_sum': order_sum,
             'order_sum': order_sum
             }
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
                {'form': e.form,
                 'order_list': order_list,
                 'group': group,
                 'order_sum': order_sum
                 }
            )
        return render(
            request,
            'order_form.html',
            {'form': OrderForm(),
             'order_list': order_list,
             'group': group,
             'order_sum': order_sum
             }
        )


def order_update_form(request, group_uuid, order_id):
    try:
        group = OrderEntryDomain.get_by_uuid(url_uuid=group_uuid)
    except DoesNotExistError:
        return HttpResponse('Hello, DoesNotExist')
    order_list = OrderDomain.get_order_by_group_uuid(group_uuid=group_uuid)
    order_sum = OrderDomain.get_order_sum(group_uuid)
    update_order = OrderDomain.get_by_orderid(id=order_id)
    if request.method == 'GET':
        form = OrderForm(
                        {'user_name': update_order.user_name,
                         'curry': update_order.curry.id
                         }
        )
        return render(
            request,
            'edit_order.html',
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
                'edit_order.html',
                {'form': e.form,
                 'order_list': order_list,
                 'group': group,
                 'update_order': update_order,
                 'order_sum': order_sum
                 }
            )
        form = OrderForm(
            {'user_name': update_order.user_name,
             'curry': update_order.curry.id
             }
        )
        order_sum = OrderDomain.get_order_sum(group_uuid)
        # return render(
        #     request,
        #     'edit_order.html',
        #     {'form': form,
        #      'order_list': order_list,
        #      'group': group,
        #      'update_order': update_order,
        #      'order_sum': order_sum
        #      }
        # )
        return HttpResponseRedirect(
            reverse('order-form', args=(group.url_uuid,))
        )

def order_delete_form(request, group_uuid, order_id):
    try:
        group = OrderEntryDomain.get_by_uuid(url_uuid=group_uuid)
    except DoesNotExistError:
        return HttpResponseRedirect('/order_entry')  # 404
    try:
        OrderDomain.delete_order(order_id)
    except DoesNotExistError:
        return HttpResponseRedirect(
        reverse('order-form', args=(group.url_uuid,))  # 404
    )
    return HttpResponseRedirect(
        reverse('order-form', args=(group.url_uuid,))
    )
