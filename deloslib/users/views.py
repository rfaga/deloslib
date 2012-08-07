#!/usr/bin/env python
# coding: UTF-8

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


from django.contrib.auth import views

from forms import NewUserForm
from delos.users.models import Person

def index(request):
    """
    Main subscription page
    """
    return render_to_response('users/index.html', {'user': request.user},
                               context_instance=RequestContext(request))


def login(request, next=None):
    #if request.user.is_authenticated():
     #   return HttpResponseRedirect('%s' % next)
    if not next or next == '/' or next == '':
        next = 'users'
    #request.GET = dict(request.GET)
    #request.GET['next'] = next
    #request.REQUEST.get('next') =  next
    
    return views.login(request, template_name='users/home.html')



### Users (a colocar em um novo app)
def edit(request):
    pass

def remove(request):
    pass

def new(request):
    if request.POST:
        form = NewUserForm(request.POST)
        if form.is_valid():
            instance = form.save()
            #Person.objects.create(user=instance)
            return HttpResponseRedirect('/users/login')
    else:
        form = NewUserForm()
    return render_to_response('users/generic_form.html', {'form': form, 'title': 'Criar uma conta',
                                                    }, 
                              context_instance=RequestContext(request))
    
# Home geral do Delos
@login_required
def home(request):
    return render_to_response('users/home.html', context_instance=RequestContext(request))
