# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from openpyxl import Workbook
from django.http import HttpResponse
from openpyxl.writer.excel import save_virtual_workbook 
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
#from exportToexcel import *
from .models import *
from datetime import *
from django.db.models import Sum

def index(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('admin:index'))
	reqmonth=request.POST.get('month')
	reqbooktype=request.POST.get('booktype')
	#print str(reqmonth)+str(reqbooktype)
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
	wb = Workbook()
	ws = wb.active
	ws.append(["日期","时间","账务类型","类型", "详细类型", "金额","备注"])
	reqmonth=request.GET.get('month')
	reqbooktype=request.GET.get('booktype')
	allObj=getItems(reqmonth,reqbooktype)
	for item in allObj:
		json=item.toJson()
		ws.append([json['time'].date().isoformat(),json['time'].strftime('%H:%M'),json['inout'],json['type'].name,json['subtype'].name,json['money'],json['memo']])
	response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = 'attachment; filename='+date.today().isoformat()+'.xlsx'
	return response

def subTypeaggr(request):
	reqmonth,reqbooktype=getSearchParam(request)
	#print reqmonth
	if nvlcheck(reqmonth):
		reqmonth=getCurrentMonth()

	subtype_list=getItems(reqmonth,reqbooktype).values('subtype').annotate(moneyTotal=Sum('money'))
	result_list=[]
	for item in subtype_list:
		subtype=BookSubType.objects.get(id=item['subtype'])
		result_list.append({'subid':item['subtype'],'subname':subtype.name,'typename':subtype.type.name,'money':item['moneyTotal']})
	template = loader.get_template('book/subTypeaggr.html')
	booktype=BookType.objects.all()
	context = {'items':result_list,"booktype":booktype,"months":getMonthList()}
	if not nvlcheck(reqmonth):
		context['reqmonth']=reqmonth
	if not nvlcheck(reqbooktype):
		context['reqbooktype']=int(reqbooktype)
	return HttpResponse(template.render(context, request))

def downloadSubtype(request):
	wb = Workbook()
	ws = wb.active
	ws.append(["月份","大类","小类","金额"])
	reqmonth=request.GET.get('month')
	reqbooktype=request.GET.get('booktype')
	if nvlcheck(reqmonth):
		reqmonth=getCurrentMonth()
	subtype_list=getItems(reqmonth,reqbooktype).values('subtype').annotate(moneyTotal=Sum('money'))
	for item in subtype_list:
		subtype=BookSubType.objects.get(id=item['subtype'])
		ws.append([reqmonth,subtype.type.name,subtype.name,item['moneyTotal']])
	response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = 'attachment; filename=subtype'+date.today().isoformat()+'.xlsx'
	return response


def getSearchParam(request):
	reqmonth=request.POST.get('month')
	reqbooktype=request.POST.get('booktype')
	return (reqmonth,reqbooktype)

def getCurrentMonth():
	td=date.today()
	monthbegin=date(td.year,td.month,1)
	return monthbegin.strftime('%Y%m')
def getMonthList():
	td=date.today()
	monthbegin=date(td.year,td.month,1)
	monthlist=[monthbegin.strftime('%Y%m')]
	for x in range(1,10):
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