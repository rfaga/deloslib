#!/usr/bin/env python
# coding: UTF-8

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from django.contrib.auth import views

from forms import NewUserForm, PasswordChangeForm
from models import Person

from django.core.mail import send_mail
from django.views.decorators.cache import never_cache
import urlparse
from django.contrib.auth.models import User


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
    if request.POST and not User.objects.filter(email=request.POST.get('username', None)):
        no_user = True
    ans = views.login(request, template_name='users/login_base.html', extra_context={'next': next, 'no_user': no_user})
    if next and request.user.is_authenticated():
        return HttpResponseRedirect(next)
    else:
        return ans


def logout(request):
    next_page = _clear_url(request, request.GET.get('next', None) )
    return views.logout(request, next_page=next_page)

### Users (a colocar em um novo app)
def edit(request):
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
            person = Person.objects.get(user=user)
            msg = render_to_response('users/email_newuser.html', {'name': person.name})
            send_mail(u"Criação de conta no Delos", msg, 'setinfo@sc.usp.br', [user.email,] , fail_silently=False)
            password = request.POST['password1']
            next = _clear_url(request, request.POST.get('next', '') )
            request.POST = QueryDict('username=%s&password=%s'% (user.username, password) )
        
            return login(request, next)
    else:
        form = NewUserForm()
    data['form'] = form
    return render_to_response('users/create.html', data, context_instance=RequestContext(request))
    
# Home geral do Delos
def home(request):
    return render_to_response('users/home.html', context_instance=RequestContext(request))
