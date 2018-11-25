import django.db

from .models import Order
from .forms import OrderForm
from .exceptions import FormError


class OrderDomain:
    def post_order(request_order):
        form = OrderForm(request_order)
        form.is_valid()
        user_name = form.cleaned_data['user_name']
        selected_curry = form.cleaned_data['curry']
        curry_id = int(selected_curry)
        try:
            Order.create(user_name, curry_id)
        except django.db.IntegrityError:
            form.add_error('user_name', '既に登録しているユーザー名は登録できません')
            raise FormError(form)
