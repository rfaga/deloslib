'''
Created on 25/11/2010

@author: faga
'''
from django import template

register = template.Library()

@register.filter
def in_group(user, groups):
    """Returns a boolean if the user is in the given group, or comma-separated
    list of groups.

    Usage::

        {% if user|in_group:"Friends" %}
        ...
        {% endif %}

    or::

        {% if user|in_group:"Friends,Enemies" %}
        ...
        {% endif %}

    """
    group_list = (groups).split(',')
    try:
#        print group_list, user.groups.filter(), user.groups.values('name'), user

        return bool(user.groups.filter(name__in=group_list).values('name'))
    except:
        return False

@register.filter
def is_full(acc):
    """Returns a boolean if the account is completely filled

    Usage::

        {% if acc|is_full %}
        ...
        {% endif %}

    or::

        {% if user|in_group:"Friends,Enemies" %}
        ...
        {% endif %}

    """
    try:
        if acc.rg and acc.undergrad and acc.cv and acc.deposit:
            if acc.program.type == u"M":
                return True
            elif acc.masters:
                return True
    except:
        pass
    return False