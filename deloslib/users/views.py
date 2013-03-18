#!/usr/bin/env python
# coding: UTF-8

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from django.contrib.auth import views

from forms import NewUserForm, PasswordChangeForm
from models import UserAccount, Role, Unidade

from deloslib.users import send_mail
from django.views.decorators.cache import never_cache
import urlparse
#from django.contrib.auth.models import User
from django.conf import settings
from deloslib.users.forms import CustomizedAuthenticationForm, ContactForm
from django.core.urlresolvers import reverse


def _clear_url(request, redirect_to):
    # Use default setting if redirect_to is empty
    if not redirect_to:
        return '/'
    # Heavier security check -- don't allow redirection to a different
    # host.
    netloc = urlparse.urlparse(redirect_to)[1]
    if netloc and netloc != request.get_host():
        return '/'
    else:
        return redirect_to


def index(request):
    """
    Main subscription page
    """
    return render_to_response('users/index.html', {'user': request.user},
                               context_instance=RequestContext(request))


def login(request, next=None):
    next = next or request.GET.get('next', request.POST.get('next', ''))
    if not next or next == '/' or next == '':
        next = None
    next = _clear_url(request, next)
    no_user = False
    if request.POST and not UserAccount.objects.filter(email=request.POST.get('username', None)):
        no_user = True
    ans = views.login(request, template_name='users/login_base.html', authentication_form=CustomizedAuthenticationForm, extra_context={'next': next, 'no_user': no_user})
    if next and request.user.is_authenticated():
        return HttpResponseRedirect(next)
    else:
        return ans


def logout(request):
    return views.logout(request, next_page='/')


@login_required()
def edit(request):
    """
    Change password only, for now...
    """
    if request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse('')
    else:
        form = PasswordChangeForm(user=request.user)
    return render_to_response('users/change_password.html', {'form': form}, context_instance=RequestContext(request))
                                                          
                                                          
def remove(request):
    pass

@never_cache
def new(request, usp=None):
    data = {}
    if usp:
        data['usp'] = True
    if "next" in request.POST:
        data['next'] = _clear_url(request, request.POST['next'])

    if "create" in request.POST:        
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            try:
                send_mail(_(u"Criação de conta no Delos"), user, "users/email_newuser.html", {'name': user.name})
            except:
                pass # mail couldn't be sent, probably email is wrong... what should I do oh Lord?
            
            password = request.POST['password1']
            next = _clear_url(request, request.POST.get('next', '') )
            request.POST = QueryDict('username=%s&password=%s'% (user.identification, password) )

            return login(request, next)
    else:
        form = NewUserForm()
    data['form'] = form
    return render_to_response('users/create.html', data, context_instance=RequestContext(request))
    
# Delos home
def home(request):
    return render_to_response('users/home.html', context_instance=RequestContext(request))

# Contact page
def contact(request):
    submit = False
    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_mail()
            submit = True
    else:
        args = {}
        if request.user.is_authenticated():
            args['initial'] = {'name': request.user.name, 'email': request.user.email}
        form = ContactForm(**args)
    return render_to_response('users/contact.html', {'form': form, 'submit': submit}, context_instance=RequestContext(request))


# trocar unidade
@login_required
def unity_change(request, abbr):
    query = Role.objects.filter(unidade__abbreviation=abbr, person=request.user)
    if query:
        request.user.unidade = Unidade.objects.get(abbreviation=abbr)
        request.user.save()
    return redirect(reverse('home'))
