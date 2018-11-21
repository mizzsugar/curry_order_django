from django.db import models


class Curry(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()


class Order(models.Model):
    curry = models.ForeignKey(Curry, on_delete=models.CASCADE)
    amount = models.IntegerField()