import django.db

from .models import OrderEntry, Order
from .forms import OrderEntryForm, OrderForm
from .exceptions import FormError


class GroupEntryDomain:
    def register_group(request_group):
        form = OrderEntryForm(request_group)
        form.is_valid()
        group_name = form.cleaned_data['group']
        group = OrderEntry.create(group_name)
        return group

    def get_by_uuid(url_uuid):
        group =  OrderEntry.get_by_uuid(url_uuid)
        return group


class OrderDomain:
    def post_order(request_order):
        form = OrderForm(request_order)
        form.is_valid()
        user_name = form.cleaned_data['user_name']
        selected_curry = form.cleaned_data['curry']
        print(selected_curry)
        curry_id = int(selected_curry)
        try:
            Order.create(user_name, curry_id)
        except django.db.IntegrityError:
            form.add_error('user_name', '既に登録しているユーザー名は登録できません')
            raise FormError(form)
