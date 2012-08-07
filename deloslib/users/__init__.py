#!/usr/bin/env python
# coding: UTF-8

def inGroup(user, groups):
    """
    returns if an user is in a group list or not.
    
    ex: inGroup(user, ['group1', 'admingroup1'])
    """
    if user.is_anonymous():
        return False
    return bool(user.groups.filter(name__in=groups).count())