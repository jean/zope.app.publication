##############################################################################
#
# Copyright (c) Zope Foundation and Contributors.
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
from zope.testing import doctest, cleanup
import unittest
import zope.app.publication.browser
import zope.component
import zope.publisher.interfaces.browser

class Proxy:

    def __init__(self, context):
        print "Proxy called"
        self.context = context

class Publication(zope.app.publication.browser.BrowserPublication):

    def proxy(self, ob):
        return Proxy(ob)


class Sample:
    "Sample object for testing"

class Response:
    def reset(self):
        pass
    def handleException(self, *args):
        pass

class Request:
    principal = None
    method = 'GET'
    def __init__(self):
        self.annotations = {}
        self.response = Response()
    def hold(self, ob):
        pass
    def getTraversalStack(self):
        return []
    def getURL(self):
        return '/'

class DB:
    def open(self):
        return self
    def root(self):
        return self
    def get(self, key, default=None):
        assert key == 'Application'
        return Sample()
    def close(self):
        pass

class Publisher:

    def __init__(self, context, request):
        self.context = context

    def browserDefault(self, request):
        return self.context, ['foo']

def proxy_control():
    """You can override proxy control in a subclass

    This test makes sure the override is called in the cases where the
    publication wants to call ProxyFactory.

    >>> cleanup.cleanUp()

    >>> zope.component.provideAdapter(
    ...     Publisher, (Sample, Request),
    ...     zope.publisher.interfaces.browser.IBrowserPublisher)

    >>> pub = Publication(DB())
    >>> request = Request()

    >>> ob = pub.getApplication(request)
    Proxy called
    >>> isinstance(ob, Proxy) and isinstance(ob.context, Sample)
    True

    >>> sample = Sample()
    >>> ob, path = pub.getDefaultTraversal(request, sample)
    Proxy called
    >>> isinstance(ob, Proxy) and ob.context == sample and path == ['foo']
    True

    >>> pub.handleException(sample, request, (ValueError, ValueError(), None))
    Proxy called

    >>> cleanup.cleanUp()
    """

def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite(),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
