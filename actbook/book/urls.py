from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^toexcel', views.downloadExcel, name='toexcel'),
]