from django.db import models


class Curry(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()

    def is_over_0(self):
        return self.price > 0


class Order(models.Model):
    curry = models.ForeignKey(Curry, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def has_ordered(self):
        return self.amount > 0


