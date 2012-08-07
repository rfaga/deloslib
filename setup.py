#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='delos-users',
    version='0.1',
    description='Delos Account/users module for Django.',
    author='Roberto Faga',
    author_email='rfaga@usp.br',
    long_description=open('README.md', 'r').read(),
    url='http://github.com/rfaga/delos-users',
    packages=[
        'deloslib',
        'deloslib.users',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
