#!/usr/bin/env python
# coding: UTF-8
from django.db import models
from django.db.models.fields.files import FileField

from deloslib import fields

class CustomQuerySetManager(models.Manager):
    """A re-usable Manager to access a custom QuerySet (thx to T. Stone)"""
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_queryset(), attr, *args)

    def get_queryset(self):
        return self.model.QuerySet(self.model)
    
class PDFModelField(FileField):    
    def formfield(self, **kwargs):
        defaults = {'form_class': fields.PDFField, 'max_length': self.max_length}
        # If a file has been provided previously, then the form doesn't require
        # that a new file is provided this time.
        # The code to mark the form field as not required is used by
        # form_for_instance, but can probably be removed once form_for_instance
        # is gone. ModelForm uses a different method to check for an existing file.
        if 'initial' in kwargs:
            defaults['required'] = False
        defaults.update(kwargs)
        return super(PDFModelField, self).formfield(**defaults)
    
    
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^deloslib\.models\.PDFModelField"])
