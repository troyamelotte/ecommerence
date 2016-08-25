from django.conf.urls import url, include
from django.conf.urls.static import static
from . import views
from django.conf import settings
urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin$', views.admin),
    url(r'^login$', views.login),
    url(r'^dashboard/orders$', views.orders),
    url(r'^dashboard/products$', views.products),
    url(r'^logout$', views.logout),
    url(r'^new$', views.new),
    url(r'^addproduct$', views.addproduct),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^editproduct/(?P<id>\d+)$', views.editproduct),
    url(r'^filter/(?P<id>\d+)$', views.filter),
    url(r'^product/(?P<id>\d+)$', views.viewproduct),
    url(r'^addcart/(?P<id>\d+)$', views.addcart),
    url(r'^checkout$', views.checkout),
    url(r'^deletecart$', views.deletecart),
    url(r'^order/new/(?P<total>\d.+)$', views.ordernew),
    url(r'^order/view/(?P<id>\d+)$', views.vieworder)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
