from django.conf.urls import url

from . import views

app_name = 'coffee'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^order/$', views.order_drink, name='order_drink'),
]