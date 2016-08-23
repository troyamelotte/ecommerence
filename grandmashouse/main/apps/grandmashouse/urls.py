from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin$', views.admin),
    url(r'^login$', views.login),
    url(r'^dashboard/orders$', views.orders),
    url(r'^dashboard/products$', views.products),
    url(r'^logout$', views.logout),
]
