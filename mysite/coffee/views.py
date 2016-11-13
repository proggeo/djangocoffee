from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import loader
from .models import *


def index(request):
    drinks = Drink.objects.all()
    ingredients = Ingredient.objects.all()
    context = {'drinks': drinks, 'ingredients': ingredients}
    return render(request, 'coffee/index.html', context)


def order_drink(request):
    try:
        selected_drink = get_object_or_404(Drink, pk=request.POST['choice'])
        print(request.POST)
    except:
        return render(request, 'coffee/', {
            'message': 'You didn\'t select a drink',
        })
    else:
        try:
            user = User.objects.get(user_name=request.POST['user'])
        except User.DoesNotExist:
            user = User(user_name=request.POST['user'])
            user.save()
        order_sum = selected_drink.price
        selected_drink.amount_left -= 1
        selected_drink.save()
        order = Order(user=user, drink=selected_drink, order_sum=order_sum, date=timezone.now())
        order.save()
        if 'ingredient' in request.POST:
            for i in request.POST.getlist(key='ingredient'):
                ingredient = get_object_or_404(Ingredient, pk=i)
                order_sum += ingredient.price
                ingredient.amount_left -= 1
                order.ingredients.add(ingredient)
        order.order_sum = order_sum
        order.save()
        return HttpResponseRedirect('/coffee/')
