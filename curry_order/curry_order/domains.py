from .models import Order
from .forms import OrderForm


class OrderDomain:
    def post_order(request_order):
        form = OrderForm(request_order)
        form.is_valid()
        selected_curry = form.cleaned_data['curry']
        curry_id = int(selected_curry)
        print(curry_id)
        Order.create(curry_id)
