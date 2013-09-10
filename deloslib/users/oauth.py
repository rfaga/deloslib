#!/usr/bin/env python
# coding: UTF-8

from requests_oauthlib import OAuth1Session
from django.shortcuts import redirect
from models import UserAccount
from views import clear_url, login
import random, string
from django.conf import settings
from django.contrib.auth import login as raw_login
from backends import EmailAuthBackend

BASE_URL = 'https://labs.uspdigital.usp.br/wsusuario/oauth/'

REQUEST_TOKEN_URL = BASE_URL + 'request_token'
AUTHORIZE_URL = BASE_URL + 'authorize'
ACCESS_TOKEN_URL = BASE_URL + 'access_token'
USER_DATA_URL = BASE_URL + 'usuariousp'

def request_authorization(request):
    oauth = OAuth1Session(settings.USP_CLIENT_KEY, client_secret=settings.USP_CLIENT_SECRET)
    fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')
    request.session['usp_resource_owner_key'] = resource_owner_key
    request.session['usp_resource_owner_secret'] = resource_owner_secret
    request.session['usp_next'] = clear_url(request, request.POST.get('next', '') )

    authorization_url = oauth.authorization_url(AUTHORIZE_URL)
    return redirect( authorization_url )

def complete_authorization(request):
    oauth_response = request.GET
    verifier = oauth_response.get('oauth_verifier')
 
    resource_owner_key = request.session.get('usp_resource_owner_key', None)
    resource_owner_secret = request.session.get('usp_resource_owner_secret', None)
    oauth = OAuth1Session(settings.USP_CLIENT_KEY, client_secret=settings.USP_CLIENT_SECRET,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
 
    try:
        oauth_tokens = oauth.fetch_access_token(ACCESS_TOKEN_URL)
    except ValueError:
        return request_authorization(request)
 
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')
 
 
    oauth = OAuth1Session(settings.USP_CLIENT_KEY, client_secret=settings.USP_CLIENT_SECRET,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    response = oauth.post(USER_DATA_URL).json()
    user_data = {
        'identification': response['loginUsuario'],
        'name': response['nomeUsuario'],
        'email': response['emailPrincipalUsuario'],
    }
    
    query = UserAccount.objects.filter(
        identification=user_data['identification'],
    )
    if query and len(query) == 1:
        user = query[0]
    else:
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
        user = UserAccount.objects.create(
            identification = user_data['identification'],
            name = user_data['name'],
            email = user_data['email'],
            password = password,
        )
    user.backend = 'deloslib.users.backends.EmailAuthBackend'
    next = clear_url(request, request.session.get('usp_next', ''))
    raw_login(request, user)
    return redirect(next)
    
