'''
Created on 01/11/2011

@author: faga
'''
#!/usr/bin/env python

from django.conf.urls.defaults import patterns, url

from django.conf import settings

#import django.contrib.auth.views

urlpatterns = patterns('deloslib.users.views',
    url(r'^login/(?P<next>.*)$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'), 
    url(r'^new/(?P<usp>.*)$', 'new', name='new_user'),
    url(r'^edit$', 'edit', name='edit_user'),
       

)

urlpatterns += patterns('django.contrib.auth.views',
    (r'^password_reset$', 'password_reset', {'template_name': 'users/generic_form.html',
                                             'email_template_name': 'users/password_reset_email.html',
                                             'subject_template_name': 'users/password_reset_subject.txt', 
                                             'post_reset_redirect':'/users/login', 
                                             'from_email': settings.EMAIL_FROM}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$', 'password_reset_confirm', {'template_name': 'users/generic_form.html', 'post_reset_redirect':'/users/login'}),
 )