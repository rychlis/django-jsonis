#!/usr/bin/env python

from setuptools import setup

setup(
    name='django-jsonis',
    version='0.1.9',
    description='Django JSON Utils',
    author='Tomas Rychlik',
    author_email='rychlis@rychlis.cz',
    packages=['jsonis', 'jsonis.templatetags', 'jsonis.jwt'],
    license='MIT',
    url='https://github.com/rychlis/django-jsonis',
    install_requires=[
        'Django >= 1.4.0',
        'PyJWT'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
