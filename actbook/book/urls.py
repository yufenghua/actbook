from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^toexcel', views.downloadExcel, name='toexcel'),
    url(r'^add', views.add, name='add'),
]