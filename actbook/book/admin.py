# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

admin.site.register(BookType)
admin.site.register(BookSubType)
admin.site.register(BookItem)

