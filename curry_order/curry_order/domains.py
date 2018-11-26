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
