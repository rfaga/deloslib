#!/usr/bin/env python
# coding: UTF-8

from django.core.exceptions import SuspiciousOperation
import os

def skip_suspicious_operations(record):
    if record.exc_info:
        exc_value = record.exc_info[1]
        if isinstance(exc_value, SuspiciousOperation):
            return False
    return True


def get_base_settings():
    return os.path.realpath( os.path.dirname(os.path.realpath(__file__)) + '/base_settings.py' )
