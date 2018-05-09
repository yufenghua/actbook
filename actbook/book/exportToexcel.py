# -*- coding: utf-8 -*-
from .models import BookItem
from openpyxl import Workbook
from datetime import date
from django.http import HttpResponse
from openpyxl.writer.excel import save_virtual_workbook 

def exportToExcel():
	wb = Workbook()
	ws = wb.active
	ws.append(["日期","时间","账务类型","类型", "详细类型", "金额","备注"])
	allObj=BookItem.objects.all()
	for item in allObj:
		json=item.toJson()
		ws.append([json['time'].date().isoformat(),json['time'].strftime('%H:%M'),json['inout'],json['type'].name,json['subtype'].name,json['money'],json['memo']])
	response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = 'attachment; filename'+date.today().isoformat()+'.xlsx'
	return response

	
	
	