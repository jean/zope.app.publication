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
"""Browser Publication Tests

$Id$
"""
import unittest

from zope.app.tests import ztapi
from StringIO import StringIO

from zope.exceptions import ForbiddenAttribute
from zope.interface import Interface, implements

from zope.publisher.publish import publish
from zope.publisher.browser import TestRequest
from zope.app.publisher.browser import BrowserView
from zope.publisher.interfaces.browser import IBrowserPublisher

from zope.proxy import removeAllProxies, getProxiedObject
from zope.security.proxy import Proxy
from zope.security.checker import defineChecker, NamesChecker

from zope.app.security.principalregistry import principalRegistry

from zope.app.publication.browser import BrowserPublication
from zope.app.publication.traversers import TestTraverser
from zope.app.publication.tests.test_zopepublication \
     import BasePublicationTests as BasePublicationTests_

from persistent import Persistent

def foo():
    "I am an otherwise empty docstring."
    return '<html><body>hello base fans</body></html>'

class DummyPublished:
    implements(IBrowserPublisher)

    def publishTraverse(self, request, name):
        if name == 'bruce':
            return foo
        raise KeyError, name

    def browserDefault(self, request):
        return self, ['bruce']



class DummyView(DummyPublished, BrowserView):

    __Security_checker__ = NamesChecker(["browserDefault", "publishTraverse"])


class BasePublicationTests(BasePublicationTests_):

    def _createRequest(self, path, publication, **kw):
        request = TestRequest(PATH_INFO=path, **kw)
        request.setPublication(publication)
        return request

class SimpleObject:
    def __init__(self, v):
        self.v = v

class I1(Interface):
    pass

class mydict(dict):
    implements(I1)


class O1(Persistent):
    implements(I1)


class BrowserDefaultTests(BasePublicationTests):
    """
    test browser default

    many views lead to a default view
    <base href="/somepath/@@view/view_method">

    """
    klass = BrowserPublication

    def testBaseTagNoBase(self):
        self._testBaseTags('/somepath/@@view/', '')

    def testBaseTag1(self):
        self._testBaseTags('/somepath/@@view',
                           'http://127.0.0.1/somepath/@@view/bruce')

    def testBaseTag2(self):
        self._testBaseTags('/somepath/',
                           'http://127.0.0.1/somepath/@@view/bruce')

    def testBaseTag3(self):
        self._testBaseTags('/somepath',
                           'http://127.0.0.1/somepath/@@view/bruce')



    def _testBaseTags(self, url, expected):
        # Make sure I1 and O1 are visible in the module namespace
        # so that the classes can be pickled.

        pub = BrowserPublication(self.db)

        ztapi.browserView(I1, 'view', DummyView)
        ztapi.setDefaultViewName(I1, 'view')
        ztapi.browserViewProviding(None, TestTraverser, IBrowserPublisher)

        ob = O1()

        ## the following is for running the tests standalone
        principalRegistry.defineDefaultPrincipal(
            'tim', 'timbot', 'ai at its best')

        # now place our object inside the application
        from transaction import get_transaction

        connection = self.db.open()
        app = connection.root()['Application']
        app.somepath = ob
        get_transaction().commit()
        connection.close()

        defineChecker(app.__class__, NamesChecker(somepath='xxx'))

        req = self._createRequest(url, pub)
        response = req.response

        publish(req, handle_errors=0)

        self.assertEqual(response.getBase(), expected)


    def _createRequest(self, path, publication, **kw):
        request = TestRequest(PATH_INFO=path, **kw)
        request.setPublication(publication)
        return request



class BrowserPublicationTests(BasePublicationTests):

    klass = BrowserPublication

    def testAdaptedTraverseNameWrapping(self):

        class Adapter:
            " "
            implements(IBrowserPublisher)
            def __init__(self, context, request):
                self.context = context
                self.counter = 0

            def publishTraverse(self, request, name):
                self.counter += 1
                return self.context[name]

        ztapi.browserViewProviding(I1, Adapter, IBrowserPublisher)
        ob = mydict()
        ob['bruce'] = SimpleObject('bruce')
        ob['bruce2'] = SimpleObject('bruce2')
        pub = self.klass(self.db)
        ob2 = pub.traverseName(self._createRequest('/bruce', pub), ob, 'bruce')
        self.assertRaises(ForbiddenAttribute, getattr, ob2, 'v')
        self.assertEqual(removeAllProxies(ob2).v, 'bruce')

    def testAdaptedTraverseDefaultWrapping(self):
        # Test default content and make sure that it's wrapped.
        class Adapter:
            implements(IBrowserPublisher)
            def __init__(self, context, request):
                self.context = context

            def browserDefault(self, request):
                return (self.context['bruce'], 'dummy')

        ztapi.browserViewProviding(I1, Adapter, IBrowserPublisher)
        ob = mydict()
        ob['bruce'] = SimpleObject('bruce')
        ob['bruce2'] = SimpleObject('bruce2')
        pub = self.klass(self.db)
        ob2, x = pub.getDefaultTraversal(self._createRequest('/bruce',pub), ob)
        self.assertEqual(x, 'dummy')
        self.assertRaises(ForbiddenAttribute, getattr, ob2, 'v')
        self.assertEqual(removeAllProxies(ob2).v, 'bruce')

    # XXX we no longer support path parameters! (At least for now)
    def XXXtestTraverseSkinExtraction(self):
        class I1(Interface): pass
        class C:
            implements(I1)
        class BobView(DummyView): pass

        pub = self.klass(self.db)
        ob = C()
        ztapi.browserView(I1, 'edit', BobView)

        r = self._createRequest('/@@edit;skin=zmi',pub)
        ob2 = pub.traverseName(r , ob, '@@edit;skin=zmi')
        self.assertEqual(r.getPresentationSkin(), 'zmi')
        self.assertEqual(ob2.__class__ , BobView)

        r = self._createRequest('/@@edit;skin=zmi',pub)
        ob2 = pub.traverseName(r , ob, '@@edit;skin=zmi')
        self.assertEqual(r.getPresentationSkin(), 'zmi')
        self.assertEqual(ob2.__class__ , BobView)

    def testTraverseName(self):
        pub = self.klass(self.db)
        class C:
            x = SimpleObject(1)
        ob = C()
        r = self._createRequest('/x',pub)
        ztapi.browserViewProviding(None, TestTraverser, IBrowserPublisher)
        ob2 = pub.traverseName(r, ob, 'x')
        self.assertRaises(ForbiddenAttribute, getattr, ob2, 'v')
        self.assertEqual(removeAllProxies(ob2).v, 1)

    def testTraverseNameView(self):
        pub = self.klass(self.db)
        class I(Interface): pass
        class C:
            implements(I)
        ob = C()
        class V:
            def __init__(self, context, request): pass
        r = self._createRequest('/@@spam',pub)
        ztapi.browserView(I, 'spam', V)
        ob2 = pub.traverseName(r, ob, '@@spam')
        self.assertEqual(ob2.__class__, V)

    def testTraverseNameServices(self):
        pub = self.klass(self.db)
        class C:
            def getSiteManager(self):
                return SimpleObject(1)
        ob = C()
        r = self._createRequest('/++etc++site',pub)
        ob2 = pub.traverseName(r, ob, '++etc++site')
        self.assertRaises(ForbiddenAttribute, getattr, ob2, 'v')
        self.assertEqual(removeAllProxies(ob2).v, 1)

    def testTraverseNameApplicationControl(self):
        from zope.app.applicationcontrol.applicationcontrol \
             import applicationController, applicationControllerRoot
        pub = self.klass(self.db)
        r = self._createRequest('/++etc++process',pub)
        ac = pub.traverseName(r,
                              applicationControllerRoot,
                              '++etc++process')
        self.assertEqual(ac, applicationController)
        r = self._createRequest('/++etc++process',pub)
        app = r.publication.getApplication(r)
        self.assertEqual(app, applicationControllerRoot)

    def testHEADFuxup(self):
        pub = self.klass(None)

        class User:
            id = 'bob'

        # With a normal request, we should get a body:
        output = StringIO()
        request = TestRequest(StringIO(''), output, {'PATH_INFO': '/'})
        request.setPrincipal(User())
        request.response.setBody("spam")
        pub.afterCall(request, None)
        request.response.outputBody()
        self.assertEqual(
            output.getvalue(),
            'Status: 200 Ok\r\n'
            'Content-Length: 4\r\n'
            'Content-Type: text/plain;charset=utf-8\r\n'
            'X-Powered-By: Zope (www.zope.org), Python (www.python.org)\r\n'
            '\r\nspam'
            )

        # But with a HEAD request, the body should be empty
        output = StringIO()
        request = TestRequest(StringIO(''), output, {'PATH_INFO': '/'})
        request.setPrincipal(User())
        request.method = 'HEAD'
        request.response.setBody("spam")
        pub.afterCall(request, None)
        request.response.outputBody()
        self.assertEqual(
            output.getvalue(),
            'Status: 200 Ok\r\n'
            'Content-Length: 0\r\n'
            'Content-Type: text/plain;charset=utf-8\r\n'
            'X-Powered-By: Zope (www.zope.org), Python (www.python.org)\r\n'
            '\r\n'
            )

    def testUnicode_NO_HTTP_CHARSET(self):
        # Test so that a unicode body doesn't cause a UnicodeEncodeError
        output = StringIO()
        request = TestRequest(StringIO(''), output, {})
        request.response.setBody(u"\u0442\u0435\u0441\u0442")
        request.response.outputBody()
        self.assertEqual(
            output.getvalue(),
            'Status: 200 Ok\r\n'
            'Content-Length: 8\r\n'
            'Content-Type: text/plain;charset=utf-8\r\n'
            'X-Powered-By: Zope (www.zope.org), Python (www.python.org)\r\n'
            '\r\n\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')


def test_suite():
    t2 = unittest.makeSuite(BrowserPublicationTests, 'test')
    t3 = unittest.makeSuite(BrowserDefaultTests, 'test')
    return unittest.TestSuite((t2, t3))


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
