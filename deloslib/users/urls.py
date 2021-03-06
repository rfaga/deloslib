'''
Created on 01/11/2011

@author: faga
'''
#!/usr/bin/env python

from django.conf.urls import patterns, url

from django.conf import settings

#import django.contrib.auth.views

urlpatterns = patterns('deloslib.users.views',
    url(r'^login/(?P<next>.*)$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^new/(?P<usp>.*)$', 'new', name='new_user'),
    url(r'^edit$', 'edit', name='edit_user'),
    url(r'^contact$', 'contact', name='contact'),
    url(r'^force_change/(?P<next>.*)$', 'force_password_change', name='force_password_change'),
    url(r'^unidade/(?P<abbr>.*)$', 'unity_change', name='users_unity_change'),
)

urlpatterns += patterns('django.contrib.auth.views',
    (r'^password_reset$', 'password_reset', {'template_name': 'users/generic_form.html',
                                             'email_template_name': 'users/password_reset_email.html',
                                             'subject_template_name': 'users/password_reset_subject.txt',
                                             'post_reset_redirect':'/users/login',
                                             'from_email': settings.EMAIL_FROM}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$', 'password_reset_confirm', {'template_name': 'users/generic_form.html', 'post_reset_redirect':'/users/login'}),
 )

urlpatterns += patterns('deloslib.users.oauth',
    url(r'^request/usp$', 'request_authorization', name='users_request_authorization'),
    url(r'^complete/usp$', 'complete_authorization', name='users_complete_authorization'),
)
