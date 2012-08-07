'''
Created on 01/11/2011

@author: faga
'''
#!/usr/bin/env python

from django.conf.urls.defaults import patterns, url

#import gifts.accounts.views

urlpatterns = patterns('deloslib.users.views',
    url(r'^login/(?P<next>.*)$', 'login', name='login'),
    url(r'^new$', 'new', name='new_user'),
       

)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^logout$', 'logout', {'next_page': '/'}, name='logout'),                        
    (r'^password_reset$', 'password_reset', {'template_name': 'users/generic_form.html', 'post_reset_redirect':'/users/login'}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$', 'password_reset_confirm', {'template_name': 'users/generic_form.html', 'post_reset_redirect':'/users/login'}),
 )