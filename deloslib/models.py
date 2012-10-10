#!/usr/bin/env python
# coding: UTF-8
from django.db import models

class CustomQuerySetManager(models.Manager):
    """A re-usable Manager to access a custom QuerySet (thx to T. Stone)"""
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        return self.model.QuerySet(self.model)