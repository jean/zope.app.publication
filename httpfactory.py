##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id: httpfactory.py,v 1.1 2003/02/07 15:59:41 jim Exp $
"""

from zope.publisher.http import HTTPRequest
from zope.publisher.browser import BrowserRequest
from zope.publisher.xmlrpc import XMLRPCRequest

from zope.app.interfaces.startup import IPublicationRequestFactoryFactory
from zope.app.interfaces.startup import IPublicationRequestFactory

from zope.app.publication.http import HTTPPublication
from zope.app.publication.browser import BrowserPublication
from zope.app.publication.xmlrpc import XMLRPCPublication


__implements__ = IPublicationRequestFactoryFactory

__metaclass__ = type

_browser_methods = 'GET', 'POST', 'HEAD'

class HTTPPublicationRequestFactory:

    __implements__ = IPublicationRequestFactory

    def __init__(self, db):
        'See IRequestFactory'

        self._http = HTTPPublication(db)
        self._brower = BrowserPublication(db)
        self._xmlrpc = XMLRPCPublication(db)

    def __call__(self, input_stream, output_steam, env):
        'See IRequestFactory'

        method = env.get('REQUEST_METHOD', 'GET').upper()

        if method in _browser_methods:
            if (method == 'POST' and
                env.get('CONTENT_TYPE', '').startswith('text/xml')
                ):
                request = XMLRPCRequest(input_stream, output_steam, env)
                request.setPublication(self._xmlrpc)
            else:
                request = BrowserRequest(input_stream, output_steam, env)
                request.setPublication(self._brower)
        else:
            request = HTTPRequest(input_stream, output_steam, env)
            request.setPublication(self._http)
        
        return request

realize = HTTPPublicationRequestFactory
