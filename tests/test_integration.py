"""
Integration tests for depdag.
"""
import unittest
from depdag import DepDag


class TestInegration(unittest.TestCase):

    def test_case_1(self):
        vert = DepDag().vertices
        vert.a.depends_on('b', 'c')
        vert.b
        vert.c.depends_on('e')
        vert.d.depends_on('e')
        vert.e.depends_on('b')
        for v in [vert.a, vert.b, vert.c, vert.d, vert.e]:
            self.assertFalse(v.provided)
            self.assertFalse(v.is_resolved())

        vert.b.payload = 'some_payload'
        vert.d.payload = 'some_payload'
        self.assertFalse(vert.a.provided)
        self.assertFalse(vert.a.is_resolved())
        self.assertTrue(vert.b.provided)
        self.assertTrue(vert.b.is_resolved())
        self.assertFalse(vert.c.provided)
        self.assertFalse(vert.c.is_resolved())
        self.assertTrue(vert.d.provided)
        self.assertFalse(vert.d.is_resolved())
        self.assertFalse(vert.e.provided)
        self.assertFalse(vert.e.is_resolved())

        vert.a.payload = 'some_payload'
        vert.e.payload = 'some_payload'
        self.assertTrue(vert.a.provided)
        self.assertFalse(vert.a.is_resolved())
        self.assertTrue(vert.b.provided)
        self.assertTrue(vert.b.is_resolved())
        self.assertFalse(vert.c.provided)
        self.assertFalse(vert.c.is_resolved())
        self.assertTrue(vert.d.provided)
        self.assertTrue(vert.d.is_resolved())
        self.assertTrue(vert.e.provided)
        self.assertTrue(vert.e.is_resolved())

        vert.c.payload = 'some_payload'
        self.assertTrue(vert.a.provided)
        self.assertTrue(vert.a.is_resolved())
        self.assertTrue(vert.b.provided)
        self.assertTrue(vert.b.is_resolved())
        self.assertTrue(vert.c.provided)
        self.assertTrue(vert.c.is_resolved())
        self.assertTrue(vert.d.provided)
        self.assertTrue(vert.d.is_resolved())
        self.assertTrue(vert.e.provided)
        self.assertTrue(vert.e.is_resolved())

    def test_case_2(self):
        vert = DepDag().vertices
        vert.a.depends_on('b')
        vert.b.depends_on('c')
        vert.c.depends_on('d')
        vert.d.depends_on('e', 'f')
        vert.e
        vert.f
        vert.g.depends_on('b')
        vert.h.depends_on('g')
        vert.i.depends_on('d')
        for v in [vert.a, vert.b, vert.c, vert.d, vert.e, vert.f, vert.g, vert.h, vert.i]:
            self.assertFalse(v.provided)
            self.assertFalse(v.is_resolved())

        vert.d.payload = 'some_payload'
        vert.e.payload = 'some_payload'
        vert.g.payload = 'some_payload'
        self.assertFalse(vert.a.provided)
        self.assertFalse(vert.a.is_resolved())
        self.assertFalse(vert.b.provided)
        self.assertFalse(vert.b.is_resolved())
        self.assertFalse(vert.c.provided)
        self.assertFalse(vert.c.is_resolved())
        self.assertTrue(vert.d.provided)
        self.assertFalse(vert.d.is_resolved())
        self.assertTrue(vert.e.provided)
        self.assertTrue(vert.e.is_resolved())
        self.assertFalse(vert.f.provided)
        self.assertFalse(vert.f.is_resolved())
        self.assertTrue(vert.g.provided)
        self.assertFalse(vert.g.is_resolved())
        self.assertFalse(vert.h.provided)
        self.assertFalse(vert.h.is_resolved())
        self.assertFalse(vert.i.provided)
        self.assertFalse(vert.i.is_resolved())

        vert.b.payload = 'some_payload'
        vert.c.payload = 'some_payload'
        vert.f.payload = 'some_payload'
        self.assertFalse(vert.a.provided)
        self.assertFalse(vert.a.is_resolved())
        self.assertTrue(vert.b.provided)
        self.assertTrue(vert.b.is_resolved())
        self.assertTrue(vert.c.provided)
        self.assertTrue(vert.c.is_resolved())
        self.assertTrue(vert.d.provided)
        self.assertTrue(vert.d.is_resolved())
        self.assertTrue(vert.e.provided)
        self.assertTrue(vert.e.is_resolved())
        self.assertTrue(vert.f.provided)
        self.assertTrue(vert.f.is_resolved())
        self.assertTrue(vert.g.provided)
        self.assertTrue(vert.g.is_resolved())
        self.assertFalse(vert.h.provided)
        self.assertFalse(vert.h.is_resolved())
        self.assertFalse(vert.i.provided)
        self.assertFalse(vert.i.is_resolved())

        vert.a.payload = 'some_payload'
        vert.h.payload = 'some_payload'
        vert.i.payload = 'some_payload'
        self.assertTrue(vert.a.provided)
        self.assertTrue(vert.a.is_resolved())
        self.assertTrue(vert.b.provided)
        self.assertTrue(vert.b.is_resolved())
        self.assertTrue(vert.c.provided)
        self.assertTrue(vert.c.is_resolved())
        self.assertTrue(vert.d.provided)
        self.assertTrue(vert.d.is_resolved())
        self.assertTrue(vert.e.provided)
        self.assertTrue(vert.e.is_resolved())
        self.assertTrue(vert.f.provided)
        self.assertTrue(vert.f.is_resolved())
        self.assertTrue(vert.g.provided)
        self.assertTrue(vert.g.is_resolved())
        self.assertTrue(vert.h.provided)
        self.assertTrue(vert.h.is_resolved())
        self.assertTrue(vert.i.provided)
        self.assertTrue(vert.i.is_resolved())
