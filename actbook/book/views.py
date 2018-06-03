# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from exportToexcel import *
from .models import *
from datetime import *

def index(request):
	print request.POST
	reqmonth=request.POST.get('month')
	reqbooktype=request.POST.get('booktype')
	print str(reqmonth)+str(reqbooktype)
	book_items=getItems(reqmonth,reqbooktype)
	booktype=BookType.objects.all()
	template = loader.get_template('book/index.html')
	context = {'items':book_items,"booktype":booktype,"months":getMonthList()}
	if not nvlcheck(reqmonth):
		context['reqmonth']=reqmonth
	if not nvlcheck(reqbooktype):
		context['reqbooktype']=int(reqbooktype)
	return HttpResponse(template.render(context, request))
def downloadExcel(request):
	return exportToExcel()

def getSearchParam(request):
	pass

def getMonthList():
	td=date.today()
	monthbegin=date(td.year,td.month,1)
	monthlist=[monthbegin.strftime('%Y%m')]
	for x in xrange(1,10):
		previous_month=monthbegin - timedelta(days=1)
		monthlist.append(previous_month.strftime('%Y%m'))
		monthbegin=date(previous_month.year,previous_month.month,1)
	return monthlist
def getItems(reqmonth,reqbooktype):
	if nvlcheck(reqmonth)  and nvlcheck(reqbooktype):
		return BookItem.objects.all().order_by('-time')
	if nvlcheck(reqmonth):
		return BookItem.objects.filter(type_id=int(reqbooktype)).order_by('-time')
	if nvlcheck(reqbooktype):
		return BookItem.objects.filter(time__year=reqmonth[0:4]).filter(time__month=reqmonth[4:6]).order_by('-time')
	return BookItem.objects.filter(time__year=reqmonth[0:4]).filter(time__month=reqmonth[4:6]).filter(type_id=int(reqbooktype)).order_by('-time')

def nvlcheck(checkvalue):
	return checkvalue==None or checkvalue=='-1' or checkvalue==''