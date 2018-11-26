from django.contrib import admin

from .models import Curry, OrderEntry, Order

admin.site.register(Curry)
admin.site.register(Order)
admin.site.register(OrderEntry)
