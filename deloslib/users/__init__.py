#!/usr/bin/env python
# coding: UTF-8
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.conf import settings
from django.template import loader, Context
import smtplib, email

from django.core.mail import send_mail as core_send_mail
from django.core.mail.message import EmailMessage

from django.contrib.sites.models import Site



def send_mail(subject, recipient_persons, template_path, context_dict={}, fail_silently=False):
    temp = loader.get_template(template_path)
    context_dict['site'] = Site.objects.get_current()
    context = Context(context_dict)
    msg = temp.render(context).encode('utf-8')
    try:
        recipient_list = ["%s <%s>" % (p.name, p.user.email) for p in recipient_persons]
    except:
        recipient_list = ["%s <%s>" % (recipient_persons.name, recipient_persons.user.email)]
    
    email = EmailMessage(subject=subject, body=msg, from_email=settings.EMAIL_FROM,
                to=recipient_list)
    email.content_subtype = 'html'
    email.encoding = 'utf-8'
    
    email.send(fail_silently=fail_silently)

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