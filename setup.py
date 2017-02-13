# -*- coding: utf-8 -*-

import re
from setuptools import setup

with open('cli.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open('README.rst', 'r') as f:
    readme = f.read()
with open('HISTORY.rst', 'r') as f:
    history = f.read()

setup(
    name='cmdbikes',
    version=version,
    description='Bike sharing at your terminal',
    long_description=readme + '\n\n' + history,
    author='Lluís Esquerda',
    author_email='eskerda@gmail.com',
    url='http://github.com/eskerda/cmdbikes',
    py_modules=['cli'],
    install_requires=[
        'python-citybikes>=0.1.3',
        'click',
        'colorama',
        'geocoder',
        'iso3166',
    ],
    entry_points='''
        [console_scripts]
        cmdbikes=cli:cli
    ''',
    keywords='Citybikes bike sharing',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

)
