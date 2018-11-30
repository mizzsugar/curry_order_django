"""curry_order URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.order_entry),
    path('order_entry', views.order_entry),
    path('show_group_url/<str:group_uuid>',
         views.show_group_url,
         name='show-group-url'),
    path('order_form/<str:group_uuid>', views.order_form, name='order-form'),
    path('order_update_form/<str:group_uuid>/<int:order_id>',
         views.order_update_form
         )
]
