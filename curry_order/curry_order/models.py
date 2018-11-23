from django.db import models


class Curry(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()

    def is_over_0(self):
        return self.price > 0

    @classmethod
    def get_by_id(cls, id):
        Curry.objects.get(id=id)


class Order(models.Model):
    curry = models.ForeignKey(Curry, on_delete=models.CASCADE)
    amount = models.IntegerField()

    @classmethod
    def create(cls, curry):
        Order.objects.create(curry_id=curry, amount=1)

    @classmethod
    def list(cls):
        return Order.objects.all()

    def has_ordered(self):
        return self.amount > 0
