from rest_framework import serializers
from .models import Drink, Ingredient


class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = ('name', 'price', 'amount_left')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'price', 'amount_left')
