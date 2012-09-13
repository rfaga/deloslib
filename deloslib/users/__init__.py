#!/usr/bin/env python
# coding: UTF-8
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def inGroup(user, groups):
    """
    returns if an user is in a group list or not.
    
    ex: inGroup(user, ['group1', 'admingroup1'])
    """
    if user.is_anonymous():
        return False
    return bool(user.groups.filter(name__in=groups).count())



def role_required(app_id):
    """
    Decorator to check if user has some role to access the app 
    """
    
    def check_role(user):
        try:
            if user.is_authenticated():
                person = user.get_profile()
                role = person.get_role(app_id)
                if role:
                    return True
        except:
            pass
        raise PermissionDenied
        return False
    return user_passes_test(check_role)


def role_admin_required(app_id):
    """
    Decorator to check if user is admin in an app
    """
    
    def check_role(user):
        try:
            if user.is_authenticated():
                person = user.get_profile()
                role = person.get_role(app_id)
                if role and role.is_admin():
                    return True
        except:
            pass
        raise PermissionDenied
        return False
    return user_passes_test(check_role)