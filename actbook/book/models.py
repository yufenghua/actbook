# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible




# Create your models here.
@python_2_unicode_compatible
class BookType(models.Model):
	name=models.CharField(max_length=600)
	def __str__(self):
		return self.name
@python_2_unicode_compatible
class BookSubType(models.Model):
	name=models.CharField(max_length=600)
	type=models.ForeignKey(BookType, on_delete=models.CASCADE)
	def __str__(self):
		return self.name+self.type.name

		

# 时间 收入/支出 大类 小类 金额 备注
@python_2_unicode_compatible
class BookItem(models.Model):
	inouttype = (
        ('INPUT', '收入'),
        ('OUTPUT', '支出'),
    )
	time=models.DateTimeField("time")
	type=models.ForeignKey(BookType, on_delete=models.CASCADE)
	subtype=models.ForeignKey(BookSubType, on_delete=models.CASCADE)
	inout=models.CharField(max_length=8, choices=inouttype)
	money=models.DecimalField(max_digits=8, decimal_places=2)
	memo=models.CharField(max_length=256)
	def __str__(self):
		return self.memo
	def toJson(self):
		js={}
		js['time']=self.time
		js['type']=self.type
		js['subtype']=self.subtype
		js['inout']=self.inout
		js['money']=self.money
		js['memo']=self.memo
		return js





