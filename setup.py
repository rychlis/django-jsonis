#!/usr/bin/env python

from distutils.core import setup

setup(
    name='django-jsonis',
    version='0.1.3',
    description='Django JSON Utils',
    author='Tomas Rychlik',
    author_email='rychlis@rychlis.cz',
    packages=['jsonis', 'jsonis.templatetags'],
    license='MIT',
    url='https://github.com/rychlis/django-jsonis',
    requires=[
        'Django(>=1.4.0)',
        'PyJWT(>=0.1.6,<0.2)'
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
