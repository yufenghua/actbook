# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from exportToexcel import *
from .models import *

def index(request):
	book_items=BookItem.objects.order_by('-time')
	template = loader.get_template('book/index.html')
	context = {'items':book_items}
	return HttpResponse(template.render(context, request))
def downloadExcel(request):
	return exportToExcel()

def getSearchParam(request):
	pass
