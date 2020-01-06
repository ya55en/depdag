"""
depdag classes unit tests.
"""

import unittest

from depdag import Vertex, DepDag, names_list


class TestVertex(unittest.TestCase):

    def test_creation__test_name(self):
        vertex = Vertex('vertex_11', DepDag())
        self.assertEqual('vertex_11', vertex.name)
        self.assertFalse(vertex.has_payload())

    def test__repr__(self):
        vertex = Vertex('vertex_22', DepDag())
        expected = "<Vertex(name='vertex_22') object at 0x"
        self.assertTrue(repr(vertex).startswith(expected))

    def test__contains__(self):
        dag = DepDag()
        dag.one.depends_on('two')
        self.assertTrue('one' in dag)
        self.assertTrue('two' in dag)

    def test__iter__(self):
        dag = DepDag()
        dag.aa.depends_on('bb')
        dag.aa.depends_on('cc')
        expected = [('aa', dag.aa), ('bb', dag.bb), ('cc', dag.cc)]
        self.assertEqual(expected, list(dag))

    def test_has_payload__for_object(self):
        vertex = Vertex('vertex_33', DepDag())
        self.assertFalse(vertex.has_payload())
        vertex.payload = "any payload would do"
        self.assertTrue(vertex.has_payload())

    def test_has_payload__for_callable(self):
        vertex = Vertex('vertex_44', DepDag())
        self.assertFalse(vertex.has_payload())

        call_log = list()

        def has_payload_callback():
            call_log.append('CALLED')
            return True

        vertex.payload = has_payload_callback
        self.assertTrue(vertex.has_payload())
        self.assertEqual(['CALLED'], call_log)

    def test_depends_on__test_supporters(self):
        vertex = Vertex('vertex_0', DepDag())
        vertex.depends_on('vertex_1', 'vertex_2')
        expected = ['vertex_1', 'vertex_2']
        self.assertEqual(expected, names_list(vertex.direct_supporters()))
        vertex.depends_on('vertex_2', 'vertex_3')
        expected = ['vertex_1', 'vertex_2', 'vertex_3']
        self.assertEqual(expected, names_list(vertex.direct_supporters()))

    def test_all_supporters(self):
        dag = DepDag()
        a = Vertex('a', dag)
        a.depends_on('b')
        b = dag['b']
        b.depends_on('c')
        self.assertEqual(['b', 'c'], names_list(a.all_supporters()))

    def test_is_resolved__simplest_case(self):
        dag = DepDag()
        a = Vertex('a', dag)
        a.depends_on('b')
        self.assertFalse(a.is_resolved())
        b = dag['b']
        self.assertFalse(b.is_resolved())
        b.payload = 'payload for vert-b'
        self.assertFalse(a.is_resolved())
        self.assertTrue(b.is_resolved())
        a.payload = 'payload for vert-a'
        self.assertTrue(a.is_resolved())
        self.assertTrue(b.is_resolved())

    def test_vertex_name_is_tuple(self):
        # exercising any hashable to be used as a vertex name (PR #2)
        dag = DepDag()
        dag[('vertex_a',)].depends_on(('vertex_b',))
        self.assertEqual(
            [('vertex_b',)],
            names_list(dag[('vertex_a',)].all_supporters())
        )
        self.assertEqual([], names_list(dag[('vertex_b',)].all_supporters()))


class TestDag(unittest.TestCase):

    def test_creation(self):
        dag = DepDag()
        self.assertEqual(0, len(dag))

    def test__getitem__(self):
        dag = DepDag()
        vertex_a = dag['a']
        self.assertIsInstance(vertex_a, Vertex)
        self.assertEqual('a', vertex_a.name)

    def test__setitem__(self):
        dag = DepDag()
        with self.assertRaises(NotImplementedError):
            dag['whatever'] = Vertex('whatever', dag)

    def test__getattr__(self):
        dag = DepDag()
        vertex = dag.vertex_384
        self.assertIsInstance(vertex, Vertex)
        self.assertEqual('vertex_384', vertex.name)

    def test__setattr__(self):
        dag = DepDag()
        with self.assertRaises(AttributeError):
            dag.whatever = Vertex('whatever', dag)

    def test__call__(self):
        dag = DepDag()
        with self.assertRaisesRegex(
                AttributeError, "Vertex object has no attribute 'misspelled'"):
            dag.misspelled()

    def test_depends_on__test_supporters(self):
        dag = DepDag()
        dag.a.depends_on('b')
        self.assertEqual(['b'], names_list(dag.a.direct_supporters()))
        dag.a.depends_on('c', 'd')
        self.assertEqual(['b', 'c', 'd'], names_list(dag.a.direct_supporters()))

    def test_all_supporters(self):
        dag = DepDag()
        dag.a.depends_on('b')
        dag.b.depends_on('c')
        self.assertEqual(['b', 'c'], names_list(dag.a.all_supporters()))

    def test_all(self):
        dag = DepDag()
        dag.a.depends_on('b')
        dag.b.depends_on('c')
        self.assertEqual([dag.a, dag.b, dag.c], list(dag.all()))

    def test_is_cyclic__negative__empty_dag(self):
        dag = DepDag()
        self.assertFalse(dag.is_cyclic())

    def test_is_cyclic__negative__one_vertex(self):
        dag = DepDag()
        dag.create('a')
        self.assertEqual(1, len(dag))
        self.assertFalse(dag.is_cyclic())

    def test_is_cyclic__negative_three_vertices(self):
        dag = DepDag()
        dag.a.depends_on('b')
        dag.b.depends_on('c')
        self.assertFalse(dag.is_cyclic())

    def test_is_cyclic__positive__one_vertex(self):
        dag = DepDag()
        dag.a.depends_on('a')
        self.assertTrue(dag.is_cyclic())

    def test_is_cyclic__positive_three_vertices(self):
        dag = DepDag()
        dag.a.depends_on('b')
        dag.b.depends_on('c')
        dag.c.depends_on('a')
        self.assertTrue(dag.is_cyclic())

    def test_is_cyclic__diamond_relationship(self):
        dag = DepDag()
        dag.a.depends_on('b')
        dag.b.depends_on('c', 'd')
        dag.c.depends_on('e')
        dag.d.depends_on('e')
        dag.e.depends_on('f')
        self.assertFalse(dag.is_cyclic())


if __name__ == '__main__':
    unittest.main()
