import uuid
from django.db import models


class Curry(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    image = models.FilePathField()

    # def __str__(self):
    #     return self.name

    def is_over_0(self):
        return self.price > 0

    @classmethod
    def get_by_id(cls, id):
        Curry.objects.get(id=id)

    @classmethod
    def list(cls):
        return Curry.objects.all()


class OrderEntry(models.Model):
    group = models.CharField(max_length=20, unique=True)
    url_uuid = models.TextField(unique=True)

    @classmethod
    def create(cls, group):
        return OrderEntry.objects.create(
            group=group,
            url_uuid=uuid.uuid4().hex
        )

    @classmethod
    def get_by_uuid(cls, url_uuid):
        return OrderEntry.objects.get(url_uuid=url_uuid)

    @classmethod
    def judge_existing_group(cls, url_uuid):
        return OrderEntry.objects.filter(url_uuid=url_uuid).exists()


class Order(models.Model):
    event = models.ForeignKey(OrderEntry, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20, unique=True)
    curry = models.ForeignKey(Curry, on_delete=models.CASCADE)
    amount = models.IntegerField()

    @classmethod
    def create(cls, event, user_name, curry):
        Order.objects.create(
            event_id=event,
            user_name=user_name,
            curry_id=curry,
            amount=1
        )

    @classmethod
    def list(cls):
        return Order.objects.all()

    @classmethod
    def group_order_list(cls, group):
        return Order.objects.filter(event=group)

    @classmethod
    def get_by_id(cls, id):
        return Order.objects.get(pk=id)

    @classmethod
    def judge_existing_order(cls, id):
        return Order.objects.filter(id=id).exists()

    def has_ordered(self):
        return self.amount > 0
