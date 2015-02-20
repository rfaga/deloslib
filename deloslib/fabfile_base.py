#!/usr/bin/env python
# coding: utf8

import tempfile

from os.path import join, exists
from os import unlink, getenv

from fabric.api import *


# fabric env config

env.hosts = ['']
env.user = 'root'
env.repository_url = ''
env.production_branch = '1.0'
env.webapps_dir = ''
env.deloslib_dir = 'deloslib'
env.project_name = 'project'
env.project_dir = '' #join(env.webapps_dir)#, env.project_name)
env.virtualenv_dir = ''

def manage_py(command, use_sudo=False):
    require('hosts')
    with cd(env.project_dir):
    	if env.virtualenv_dir:
            run('source %s && python manage.py %s --settings=project.settings.live' % (env.virtualenv_dir, command), use_sudo)
        else:
            run('python manage.py %s --settings=project.settings.live' % command, use_sudo)

@task
def push():
    local('git commit -a && git push')

@task
def deploy():
    '''Atualiza o código no host com o pull, faz migrate na base e reinicia o Apache'''
    with cd(env.project_dir):
        deloslib()
        pull()
        run('find -name "*.pyc" -delete')
        migrate()
        collectstatic()
        restart()

@task
def update_install():
    with cd(env.project_dir):
        deploy()
        sudo('pip install -r requirements.txt')

@task
def collectstatic():
    with cd(env.project_dir):
        run('rm -Rf project/.staticroot/*')
        manage_py('collectstatic -l --noinput')

@task
def pull():
    ''' puxa o código no servidor '''
    with cd(env.project_dir):
        run('git pull')
        run('chown -R www-data:www-data .')

@task
def deloslib():
    ''' sincroniza a deloslib '''
    with cd(env.deloslib_dir):
        run('git pull')
        run('chown -R www-data:www-data .')

@task
def migrate():
    ''' migrates server DB'''
    with cd(env.project_dir):
        manage_py('migrate')

@task
def syncdb():
    with cd(env.project_dir):
        manage_py('syncdb')


@task
def restart():
    '''Reinicia o Apache'''
    sudo('apache2ctl graceful')
