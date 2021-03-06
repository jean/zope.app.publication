##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################

version = '3.14.1dev'

import os
from setuptools import setup, find_packages


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


TEST_REQUIREMENTS = [
    'zope.annotation',
    'zope.app.appsetup >= 3.14.0',
    'zope.app.http >= 3.10',
    'zope.app.wsgi >= 3.12',
    'zope.applicationcontrol>=3.5.0',
    'zope.browserpage',
    'zope.login',
    'zope.password',
    'zope.principalregistry',
    'zope.security>=4.0.0a1',
    'zope.securitypolicy',
    'zope.site',
    'zope.testing',
    'zope.testrunner',
    'ZODB3>=3.10dev',
]

setup(name='zope.app.publication',
    version=version,
    author='Zope Corporation and Contributors',
    author_email='zope-dev@zope.org',
    description='Zope publication',
    long_description=(
        read('README.txt')
        + '\n\n' +
        read('CHANGES.txt')
    ),
    license='ZPL 2.1',
    keywords="zope publication",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3',
    ],
    url='http://pypi.python.org/pypi/zope.app.publication',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zope', 'zope.app'],
    extras_require=dict(test=TEST_REQUIREMENTS),
    install_requires=[
        'zope.interface',
        'zope.authentication',
        'zope.component',
        'zope.error',
        'zope.browser>=1.2',
        'zope.location',
        'zope.publisher>=4.0.0a2',
        'zope.traversing>=3.9.0',
        'zope.untrustedpython',
        'zope.i18n>=4.0.0a3',
        'transaction>=1.1.0',
        'setuptools',
    ],
    tests_require=TEST_REQUIREMENTS,
    include_package_data=True,
    zip_safe=False,
)
