#!/usr/bin/env python
# coding: UTF-8

from django.contrib import admin
from models import *

from django import forms
from admin_enhancer import admin as enhanced_admin


admin.site.register(Unidade, admin.ModelAdmin)

class EnhancedModelAdmin(enhanced_admin.EnhancedModelAdminMixin,
                         admin.ModelAdmin):
    pass

class PersonForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.order_by('word'),)
    class Meta:
        model = Person

class RoleInline(admin.TabularInline):
    model = Role
    extra = 1
    

class PersonAdmin(EnhancedModelAdmin):
    inlines = (RoleInline,)
    readonly_fields = ('email', 'is_superuser')
    def email(self, obj):
        return obj.user.email
    def is_superuser(self, obj):
        if obj.user.is_superuser:
            return u"Sim"
        else:
            return u"Não" 
    
    is_superuser.short_description = 'Super Administrador?'
    
    
admin.site.register(Person, PersonAdmin)
#admin.site.register(Role, admin.ModelAdmin)