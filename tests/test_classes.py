"""
depdag classes unit tests.
"""

import unittest
from depdag import Vertex, VerticesMap, DepDag


class TestVertex(unittest.TestCase):

    def test_creation__test_name(self):
        vertex = Vertex('vertex_11', VerticesMap(None))
        self.assertEqual('vertex_11', vertex.name)
        self.assertFalse(vertex.provided)

    def test__repr__(self):
        vtx = Vertex('vertex_22', VerticesMap(None))
        expected = "<Vertex(name='vertex_22') object at 0x"
        self.assertTrue(repr(vtx).startswith(expected))

    def test_provide_payload(self):
        vertex = Vertex('vertex_33', VerticesMap(None))
        self.assertFalse(vertex.provided)
        vertex.payload = "any payload would do"
        self.assertTrue(vertex.provided)

    def test_depends_on__test_supporters(self):
        vtx = Vertex('vertex_0', VerticesMap(None))
        vtx.depends_on('vertex_1', 'vertex_2')
        expected = ['vertex_1', 'vertex_2']
        self.assertEqual(expected, vtx.supporters(recurse=False))
        vtx.depends_on('vertex_2', 'vertex_3')
        expected = ['vertex_1', 'vertex_2', 'vertex_3']
        self.assertEqual(expected, vtx.supporters(recurse=False))

    def test_all_supporters(self):
        vmap = VerticesMap(None)
        a = Vertex('a', vmap)
        a.depends_on('b')
        b = vmap['b']
        b.depends_on('c')
        self.assertEqual(['b', 'c'], a.supporters(recurse=True))

    def test_is_resolved__simplest_case(self):
        vmap = VerticesMap(None)
        a = Vertex('a', vmap)
        a.depends_on('b')
        self.assertFalse(a.is_resolved())
        b = vmap['b']
        self.assertFalse(b.is_resolved())
        b.payload = 'payload for vert-b'
        self.assertFalse(a.is_resolved())
        self.assertTrue(b.is_resolved())
        a.payload = 'payload for vert-a'
        self.assertTrue(a.is_resolved())
        self.assertTrue(b.is_resolved())


class TestVerticesMap(unittest.TestCase):

    def test_creation(self):
        VerticesMap(None)

    def test__getitem__(self):
        vert = VerticesMap(None)
        vertex_a = vert['a']
        self.assertIsInstance(vertex_a, Vertex)
        self.assertEqual('a', vertex_a.name)

    def test__setitem__(self):
        vert = VerticesMap(None)
        with self.assertRaises(NotImplementedError):
            vert['whatever'] = Vertex('whatever', vert)

    def test__getattr__(self):
        vert = VerticesMap(None)
        vertex = vert.vertex_384
        self.assertIsInstance(vertex, Vertex)
        self.assertEqual('vertex_384', vertex.name)

    def test__setattr__(self):
        vert = VerticesMap(None)
        with self.assertRaises(AttributeError):
            vert.z = Vertex('z', vert)


class TestDag(unittest.TestCase):

    def test_creation(self):
        dag = DepDag()

    def test_depends_on__test_supporters(self):
        vert = DepDag().vertices
        vert.a.depends_on('b')
        self.assertEqual(['b'], vert.a.supporters(recurse=False))
        vert.a.depends_on('c', 'd')
        self.assertEqual(['b', 'c', 'd'], vert.a.supporters(recurse=False))

    def test_all_supporters(self):
        vert = DepDag().vertices
        vert.a.depends_on('b')
        vert.b.depends_on('c')
        self.assertEqual(['b', 'c'], vert.a.supporters(recurse=True))

    def test_is_cyclic__negative__empty_dag(self):
        dag = DepDag()
        self.assertFalse(dag.is_cyclic())

    def test_is_cyclic__negative__one_vertex(self):
        dag = DepDag()
        vert = dag.vertices
        vert.create('a')
        self.assertEqual(1, len(vert))
        self.assertFalse(dag.is_cyclic())

    def test_is_cyclic__negative_three_vertices(self):
        dag = DepDag()
        vert = dag.vertices
        vert.a.depends_on('b')
        vert.b.depends_on('c')
        self.assertFalse(dag.is_cyclic())

    def test_is_cyclic__positive__one_vertex(self):
        dag = DepDag()
        vert = dag.vertices
        vert.a.depends_on('a')
        self.assertTrue(dag.is_cyclic())

    def test_is_cyclic__positive_three_vertices(self):
        dag = DepDag()
        vert = dag.vertices
        vert.a.depends_on('b')
        vert.b.depends_on('c')
        vert.c.depends_on('a')
        self.assertTrue(dag.is_cyclic())


if __name__ == '__main__':
    unittest.main()
