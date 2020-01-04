"""
Integration tests for depdag.
"""
import unittest
from depdag import DepDag


class TestIntegration(unittest.TestCase):

    def test_case_1(self):
        dag = DepDag()
        dag.a.depends_on('b', 'c')
        dag.c.depends_on('e')
        dag.d.depends_on('e')
        dag.e.depends_on('b')
        for v in [dag.a, dag.b, dag.c, dag.d, dag.e]:
            self.assertFalse(v.has_payload)
            self.assertFalse(v.is_resolved())

        dag.b.payload = 'some_payload'
        dag.d.payload = 'some_payload'
        self.assertFalse(dag.a.has_payload)
        self.assertFalse(dag.a.is_resolved())
        self.assertTrue(dag.b.has_payload)
        self.assertTrue(dag.b.is_resolved())
        self.assertFalse(dag.c.has_payload)
        self.assertFalse(dag.c.is_resolved())
        self.assertTrue(dag.d.has_payload)
        self.assertFalse(dag.d.is_resolved())
        self.assertFalse(dag.e.has_payload)
        self.assertFalse(dag.e.is_resolved())

        dag.a.payload = 'some_payload'
        dag.e.payload = 'some_payload'
        self.assertTrue(dag.a.has_payload)
        self.assertFalse(dag.a.is_resolved())
        self.assertTrue(dag.b.has_payload)
        self.assertTrue(dag.b.is_resolved())
        self.assertFalse(dag.c.has_payload)
        self.assertFalse(dag.c.is_resolved())
        self.assertTrue(dag.d.has_payload)
        self.assertTrue(dag.d.is_resolved())
        self.assertTrue(dag.e.has_payload)
        self.assertTrue(dag.e.is_resolved())

        dag.c.payload = 'some_payload'
        self.assertTrue(dag.a.has_payload)
        self.assertTrue(dag.a.is_resolved())
        self.assertTrue(dag.b.has_payload)
        self.assertTrue(dag.b.is_resolved())
        self.assertTrue(dag.c.has_payload)
        self.assertTrue(dag.c.is_resolved())
        self.assertTrue(dag.d.has_payload)
        self.assertTrue(dag.d.is_resolved())
        self.assertTrue(dag.e.has_payload)
        self.assertTrue(dag.e.is_resolved())

    def test_case_2(self):
        dag = DepDag()
        dag.a.depends_on('b')
        dag.b.depends_on('c')
        dag.c.depends_on('d')
        dag.d.depends_on('e', 'f')
        dag.g.depends_on('b')
        dag.h.depends_on('g')
        dag.i.depends_on('d')
        for v in [dag.a, dag.b, dag.c, dag.d, dag.e, dag.f, dag.g, dag.h, dag.i]:
            self.assertFalse(v.has_payload)
            self.assertFalse(v.is_resolved())

        dag.d.payload = 'some_payload'
        dag.e.payload = 'some_payload'
        dag.g.payload = 'some_payload'
        self.assertFalse(dag.a.has_payload)
        self.assertFalse(dag.a.is_resolved())
        self.assertFalse(dag.b.has_payload)
        self.assertFalse(dag.b.is_resolved())
        self.assertFalse(dag.c.has_payload)
        self.assertFalse(dag.c.is_resolved())
        self.assertTrue(dag.d.has_payload)
        self.assertFalse(dag.d.is_resolved())
        self.assertTrue(dag.e.has_payload)
        self.assertTrue(dag.e.is_resolved())
        self.assertFalse(dag.f.has_payload)
        self.assertFalse(dag.f.is_resolved())
        self.assertTrue(dag.g.has_payload)
        self.assertFalse(dag.g.is_resolved())
        self.assertFalse(dag.h.has_payload)
        self.assertFalse(dag.h.is_resolved())
        self.assertFalse(dag.i.has_payload)
        self.assertFalse(dag.i.is_resolved())

        dag.b.payload = 'some_payload'
        dag.c.payload = 'some_payload'
        dag.f.payload = 'some_payload'
        self.assertFalse(dag.a.has_payload)
        self.assertFalse(dag.a.is_resolved())
        self.assertTrue(dag.b.has_payload)
        self.assertTrue(dag.b.is_resolved())
        self.assertTrue(dag.c.has_payload)
        self.assertTrue(dag.c.is_resolved())
        self.assertTrue(dag.d.has_payload)
        self.assertTrue(dag.d.is_resolved())
        self.assertTrue(dag.e.has_payload)
        self.assertTrue(dag.e.is_resolved())
        self.assertTrue(dag.f.has_payload)
        self.assertTrue(dag.f.is_resolved())
        self.assertTrue(dag.g.has_payload)
        self.assertTrue(dag.g.is_resolved())
        self.assertFalse(dag.h.has_payload)
        self.assertFalse(dag.h.is_resolved())
        self.assertFalse(dag.i.has_payload)
        self.assertFalse(dag.i.is_resolved())

        dag.a.payload = 'some_payload'
        dag.h.payload = 'some_payload'
        dag.i.payload = 'some_payload'
        self.assertTrue(dag.a.has_payload)
        self.assertTrue(dag.a.is_resolved())
        self.assertTrue(dag.b.has_payload)
        self.assertTrue(dag.b.is_resolved())
        self.assertTrue(dag.c.has_payload)
        self.assertTrue(dag.c.is_resolved())
        self.assertTrue(dag.d.has_payload)
        self.assertTrue(dag.d.is_resolved())
        self.assertTrue(dag.e.has_payload)
        self.assertTrue(dag.e.is_resolved())
        self.assertTrue(dag.f.has_payload)
        self.assertTrue(dag.f.is_resolved())
        self.assertTrue(dag.g.has_payload)
        self.assertTrue(dag.g.is_resolved())
        self.assertTrue(dag.h.has_payload)
        self.assertTrue(dag.h.is_resolved())
        self.assertTrue(dag.i.has_payload)
        self.assertTrue(dag.i.is_resolved())
