##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Publication factories.

This module provides factories for tuples (request, publication).

$Id$
"""
__docformat__ = 'restructuredtext'

from zope import component
from zope.interface import implements
from zope.app.publication.http import BaseHTTPPublication
from zope.app.publication.interfaces import IRequestPublicationFactory, ISOAPRequestFactory, ISOAPRequestFactory
from zope.app.publication import interfaces
from zope.app.publication.soap import SOAPPublication
from zope.app.publication.xmlrpc import XMLRPCPublication
from zope.app.publication.http import HTTPPublication
from zope.publisher.xmlrpc import XMLRPCRequest
from zope.app.publication.browser import BrowserPublication 
from zope.publisher.http import HTTPRequest
from zope.publisher.browser import BrowserRequest

class SOAPFactory(object):

    implements(IRequestPublicationFactory)

    def canHandle(self, environment):
        soap_req = component.queryUtility(interfaces.ISOAPRequestFactory)
        return bool(environment.get('HTTP_SOAPACTION') and soap_req)

    def getSortKey(self):
        return '1'

    def __call__(self):
        soap_req = component.queryUtility(interfaces.ISOAPRequestFactory)
        return soap_req, SOAPPublication

class XMLRPCFactory(object):

    implements(IRequestPublicationFactory)

    def canHandle(self, environment):
        return True

    def __call__(self):
        request_class = component.queryUtility(
            interfaces.IXMLRPCRequestFactory, default=XMLRPCRequest)
        return request_class, XMLRPCPublication

    def getSortKey(self):
        return '0'

class HTTPFactory(object):

    implements(IRequestPublicationFactory)

    def canHandle(self, environment):
        return True

    def getSortKey(self):
        return '0'

    def __call__(self):
        request_class = component.queryUtility(
            interfaces.IHTTPRequestFactory, default=HTTPRequest)
        return request_class, HTTPPublication

class BrowserFactory(object):

    implements(IRequestPublicationFactory)

    def canHandle(self, environment):
        return True

    def __call__(self):
        request_class = component.queryUtility(
                interfaces.IBrowserRequestFactory, default=BrowserRequest)
        return request_class, BrowserPublication

    def getSortKey(self):
        return '0'
