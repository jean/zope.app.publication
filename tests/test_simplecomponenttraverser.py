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

$Id: test_simplecomponenttraverser.py,v 1.6 2003/03/13 18:49:08 alga Exp $
"""

import unittest, sys
from zope.component.tests.request import Request
from zope.app.publication.traversers import SimpleComponentTraverser
from zope.component import getService
from zope.app.services.servicenames import Views
from zope.interface import Interface
from zope.exceptions import NotFoundError
from zope.app.tests.placelesssetup import PlacelessSetup

class I(Interface):
    pass


class Container:
    def __init__(self, **kw):
        for k in kw:
            setattr(self, k , kw[k])

    def get(self, name, default=None):
        return getattr(self, name, default)


class Request(Request):
    def getEffectiveURL(self):
        return ''


class View:
    def __init__(self, comp, request):
        self._comp = comp


class Test(PlacelessSetup, unittest.TestCase):
    def testAttr(self):
        # test container traver
        foo = Container()
        c   = Container(foo=foo)
        req = Request(I, '')

        T = SimpleComponentTraverser(c, req)

        self.assertRaises(NotFoundError , T.publishTraverse, req ,'foo')


    def testView(self):
        # test getting a view
        foo = Container()
        c   = Container(foo=foo)
        req = Request(I, '')

        T = SimpleComponentTraverser(c, req)
        getService(None,Views).provideView(None , 'foo', I, [View])

        self.failUnless(T.publishTraverse(req,'foo').__class__ is View )

        self.assertRaises(NotFoundError , T.publishTraverse, req ,'morebar')



def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(Test)


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
