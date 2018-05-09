# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from exportToexcel import *

def index(request):
    return HttpResponse("<a href='toexcel'>粗暴的下载账单吧</a>")
def downloadExcel(request):
	return exportToExcel()
