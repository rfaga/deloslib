#!/usr/bin/env python
# coding: UTF-8

from django.contrib import admin
from models import *

admin.site.register(Unidade, admin.ModelAdmin)
admin.site.register(Person, admin.ModelAdmin)
admin.site.register(Role, admin.ModelAdmin)