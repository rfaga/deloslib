#!/usr/bin/env python
# coding: UTF-8


import re, random, os
from django.utils.translation import ugettext as _
from django.template.defaultfilters import filesizeformat
from django.forms import FileField, ValidationError, forms, fields, widgets
from django.template import loader, Context
from django.contrib.auth.models import AnonymousUser
from django.utils.encoding import smart_unicode

class PDFField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.content_types = ["application/pdf", "application/x-pdf", "application/acrobat", "applications/vnd.pdf",
                              "text/pdf", "text/x-pdf"] #kwargs.pop("content_types")
        self.max_upload_size = 20971520 #kwargs.pop("max_upload_size")
        super(PDFField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):        
        data = super(PDFField, self).clean(*args, **kwargs)
        try:
            if not data:
                return
            file = data.file
            
            if data.content_type in self.content_types or ".pdf" in data._name.lower():
                if data._size > self.max_upload_size:
                    raise ValidationError(_('Tamanho do arquivo excedido de %s. Tamanho atual: %s') % (filesizeformat(self.max_upload_size), filesizeformat(data._size)))
            else:
                
                raise ValidationError(_('Tipo de arquivo nao e PDF.'))
        except AttributeError:
            pass        
            
        return data
