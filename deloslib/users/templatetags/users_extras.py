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


@register.filter
def cnpj_cpf(value):
    """
    Returns CNPJ or CPF humanized
    """
    value = str(value)
    if len(value) == 11:
        # cpf
        return value[0:3] + '.' + value[3:6] + '.' + value[6:9] + '-' + value[9:11]
    elif len(value) == 14:
        #cnpj
        return value[0:2] + '.' + value[2:5] + '.' + value[5:8] + '/' + value[8:12] + '-' + value[12:14]
    return value