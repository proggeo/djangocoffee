from django.conf.urls import url

from . import views

app_name = 'coffee'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_page/$', views.register_page, name='register_page'),
    url(r'^admin/$', views.admin_page, name='admin_page'),
    url(r'^admin_update/$', views.admin_update, name='admin_update'),
    url(r'^order_page/$', views.order_page, name='order_page'),
    url(r'^order/$', views.order_drink, name='order_drink'),
    url(r'^success/$', views.success, name='success'),

    url(r'^drink/$', views.DrinkList.as_view()),
    url(r'^drink/(?P<pk>[0-9]+)/$', views.DrinkDetail.as_view()),
    url(r'ingredient/$', views.IngredientList.as_view()),
    url(r'ingredient/(?P<pk>[0-9]+)/$', views.IngredientDetail.as_view()),
    url(r'^logout/$', views.logout, name='logout')

]