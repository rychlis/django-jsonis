#!/usr/bin/env python

from distutils.core import setup

setup(
    name='django-jsonis',
    version='0.1.0',
    description='Django JSON Utils',
    author='Tomas Rychlik',
    author_email='rychlis@rychlis.cz',
    packages=['jsonis'],
    license='MIT',
    install_requires=[
        'Django==1.6.3',
        'PyJWT==0.1.6'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
