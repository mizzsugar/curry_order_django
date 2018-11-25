from django.test import TestCase

from .models import Curry, OrderEntry, Order


class LearningTest(TestCase):
    def test_assert_equals(self):
        a = 1
        self.assertIs(a, 1)


class ModelCurryTest(TestCase):
    def test_curry_price(self):
        curry = Curry(price=0)
        self.assertIs(curry.is_over_0(), False)


class ModelOrderTest(TestCase):
    def test_order_amount(self):
        order = Order(amount=0)
        self.assertIs(order.has_ordered(), False)

    def test_get_by_uuid(self):
        group = OrderEntry(name='aaaaa', url_uuid='gefdslvbuoiueeref3')
        self.assertIs(group.get_by_uuid('gefdslvbuoiueeref3').name, 'aaaaa')