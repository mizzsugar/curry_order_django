import django.db

from .models import OrderEntry, Order
from .forms import OrderEntryForm, OrderForm
from .exceptions import FormError, DoesNotExistError


class OrderEntryDomain:
    def register_group(request_group):
        form = OrderEntryForm(request_group)
        form.is_valid()
        group_name = form.cleaned_data['group']
        group = OrderEntry.create(group_name)
        return group

    def get_by_uuid(url_uuid):
        if not OrderEntry.judge_existing_group(url_uuid=url_uuid):
            raise DoesNotExistError
        else:
            return OrderEntry.get_by_uuid(url_uuid=url_uuid)


class OrderDomain:
    def get_order_by_group_uuid(group_uuid):
        group = OrderEntry.get_by_uuid(group_uuid)
        return Order.group_order_list(group)

    def get_by_orderid(id):
        if not Order.judge_existing_order(id=id):
            raise DoesNotExistError
        else:
            return Order.get_by_id(id=id)

    def post_order(request_order, group_uuid):
        form = OrderForm(request_order)
        form.is_valid()
        user_name = form.cleaned_data['user_name']
        selected_curry = form.cleaned_data['curry']
        curry_id = int(selected_curry)
        try:
            group = OrderEntry.get_by_uuid(url_uuid=group_uuid)
        except django.core.exceptions.ObjectDoesNotExist:
            raise DoesNotExistError
        group_id = group.id
        try:
            Order.create(group_id, user_name, curry_id)
        except django.db.IntegrityError:
            form.add_error('user_name', '既に登録しているユーザー名は登録できません')
            raise FormError(form)

    #  updateは未完成。なぜかinsertされる・・・・
    def update_order(request_order, update_order):
        form = OrderForm(request_order)
        form.is_valid()
        update_order.user_name = form.cleaned_data['user_name']
        update_order.curry_id = form.cleaned_data['curry']
        try:
            update_order.save()
        except django.db.IntegrityError:
            form.add_error('user_name', '既に登録しているユーザー名は登録できません')
            raise FormError(form)
        return update_order

    def get_order_sum(group_uuid):  #1こ目が加算されない
        orders = OrderDomain.get_order_by_group_uuid(group_uuid)
        sum = 0
        for order in orders:
            sum += order.curry.price
        return sum
