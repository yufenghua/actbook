from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^toexcel', views.downloadExcel, name='toexcel'),
    url(r'^subtype', views.subTypeaggr, name='subtype'),
    url(r'^dsubtype', views.downloadSubtype, name='dsubtype'),
    
]