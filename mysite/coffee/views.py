from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import loader
from .models import *


def index(request):
    if 'type' not in request.session:
        return render(request, 'coffee/login.html')
    elif request.session['type'] == 'user':
        return HttpResponseRedirect('/coffee/order_page/')
    elif request.session['type'] == 'admin':
        return HttpResponseRedirect('/coffee/admin/')
    else:
        return render(request, 'coffee/login.html')


def register_page(request):
    return render(request, 'coffee/register.html')


def login(request):
    try:
        print(request.POST['user_name'])
        user = User.objects.get(user_name=request.POST['user_name'])
        print(user)
        print(request.POST)
    except:
        return HttpResponseRedirect('/coffee/')
    else:
        if user.password == request.POST['password']:
            request.session['user_id'] = user.id
            if user.is_admin:
                print('odmin')
                request.session['type'] = 'admin'
                return HttpResponseRedirect('/coffee/admin/')
            else:
                request.session['type'] = 'user'
                return HttpResponseRedirect('/coffee/order_page/')
        else:
            return HttpResponseRedirect('/coffee/')


def register(request):
    user_name = request.POST['user_name']
    password = request.POST['password']
    if len(user_name) < 0 or len(password) < 0:
        return HttpResponseRedirect('/coffee/')
    user = User(user_name=user_name, password=password)
    user.save()
    return HttpResponseRedirect('/coffee/')


def order_page(request):
    if 'type' not in request.session:
        return HttpResponseRedirect('/coffee/')
    drinks = Drink.objects.all()
    ingredients = Ingredient.objects.all()
    user = User.objects.get(id=request.session['user_id'])
    context = {'drinks': drinks, 'ingredients': ingredients, 'user': user}
    return render(request, 'coffee/index.html', context)


def admin_page(request):
    if 'type' not in request.session:
        return HttpResponseRedirect('/coffee/')
    elif request.session['type'] != 'admin':
        return HttpResponseRedirect('/coffee/order_page/')
    drinks = Drink.objects.all()
    ingredients = Ingredient.objects.all()
    users = User.objects.all()
    context = {
        'drinks': drinks,
        'ingredients': ingredients,
        'users': users
    }
    return render(request, 'coffee/admin.html', context)


def admin_update(request):
    print(request.POST)
    drinks = Drink.objects.all()
    ingredients = Ingredient.objects.all()
    users = User.objects.all()
    for drink in drinks:
        drink.amount_left = int(request.POST['drink'+str(drink.id)])
        drink.save()
    for ingredient in ingredients:
        ingredient.amount_left = int(request.POST['ingredient'+str(ingredient.id)])
        ingredient.save()
    for user in users:
        user.money_left = float(request.POST['user'+str(user.id)])
        user.save()
    return HttpResponseRedirect('/coffee/admin/')


def order_drink(request):
    try:
        selected_drink = get_object_or_404(Drink, pk=request.POST['choice'])
        print(request.POST)
    except:
        return HttpResponseRedirect('/coffee/order_page/')
    else:
        user = User.objects.get(id=request.session['user_id'])
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
                ingredient.save()
        order.order_sum = order_sum
        order.save()
        if user.money_left < order.order_sum:
            user.money_left -= order.order_sum
        user.save()
        return HttpResponseRedirect('/coffee/order_page/')
