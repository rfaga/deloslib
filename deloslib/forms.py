#!/usr/bin/env python
# coding: UTF-8


import re, random, os
from django.utils.translation import ugettext as _
from django.template.defaultfilters import filesizeformat
from django.forms import FileField, ValidationError, forms, fields, widgets, ModelForm
from django.template import loader, Context
from django.contrib.auth.models import AnonymousUser
from django.utils.encoding import smart_unicode
from django.utils.datastructures import SortedDict
from deloslib.fields import PDFField


class DynamicModelForm(ModelForm):
    
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields', None)
        self.custom_fields = []
        fields = {}
        initial = kwargs.pop('initial', {})
        if extra_fields:
            for name, field in create_fields(extra_fields):
                fields[name] = field
                self.custom_fields.append(name)
        
            instance = kwargs.get('instance', None)
            instance_extra_field = kwargs.get('instance_extra_field', 'extra_fields')
            if instance:
                try:
                    extra = eval(getattr(instance, instance_extra_field))
                except:
                    extra = {}
                for f in self.custom_fields:
                    initial[f] = extra.get(f, '')
        super(DynamicModelForm, self).__init__(*args, initial=initial, **kwargs)
        if fields:
            self.fields = dict(self.fields.items() + fields.items())

    def save(self, commit=True, file_saver=None):
        instance = super(DynamicModelForm, self).save(commit=False)
        d = {} 
        for x in self.custom_fields:
#            if type(x) != type(u'') and file_saver:
#                file_saver(x, self.cleaned_data[x], instance)
            d[x] = self.cleaned_data[x]
        instance.extra_fields = d
        if commit:
            instance.save()
        return instance    

def create_fields(pickled_object):
    cf = []
    for i, d in enumerate(pickled_object):
        args = {
            'label': d.get('label', 'Campo %d'%i)
        }
        name = d.get('name', 'custom_%d'%i)
        widget_args = {}
        if d['class'] == 'text':
            widget_args['attrs'] = {}
            widget_args['attrs']['cols'] = d.get('cols', '100')
            widget_args['attrs']['rows'] = d.get('rows', '2')
            cf.append( (name, fields.CharField(widget=widgets.Textarea(**widget_args), **args) ))
        elif d['class'] == 'char':
            cf.append( (name, fields.CharField(widget=widgets.TextInput(), **args) ))
        elif d['class'] == 'pdf':
            cf.append( (name, PDFField(**args)))
    return cf

def order_fields(form, fields_list):
    form.fields = SortedDict(form.fields)
    form.fields.keyOrder = fields_list
