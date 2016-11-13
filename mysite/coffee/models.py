from django.db import models
from django.utils import timezone


# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=200)

    def __str__(self):
        return self.user_name


class Drink(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    amount_left = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    amount_left = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_sum = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return str(self.date) + ': ' + self.user.user_name