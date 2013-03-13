#!/usr/bin/env python
# coding: UTF-8

from models import UserAccount

def user_post_create(signal, instance, sender, created, **kwargs):
    if created and instance.user:
        if instance.user.is_active: # if user was created by admin
            print "yes act"
            pass # send password too
        else:
            print "no act"
            pass # send no password

