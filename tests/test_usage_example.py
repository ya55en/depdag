"""
Test exercising the documentation usage examples.
"""

import unittest


class TestUsageExample(unittest.TestCase):

    def test_usage_example(self):
        from depdag import DepDag

        # Create the DAG structure and get a reference to the vertices collection:
        dag = DepDag()

        # Connect vertices with directed dependency relationships (i.e. the edges):
        dag.a.depends_on('b')
        dag.b.depends_on('d')
        dag.c.depends_on('d', 'e')
        assert not dag.is_cyclic()

        # Explore who depends on whom, recursively; prints:
        # - vert a -> all supporters: ['b', 'd']
        # - vert b -> all supporters: ['d']
        # - vert d -> all supporters: []
        # - vert c -> all supporters: ['d', 'e']
        # - vert e -> all supporters: []
        for v in dag.all():
            print("- vert", v.name, "-> all supporters:", v.supporters(recurse=True))

        # Set some payload and see which vertices are 'resolved', that is,
        # all supporters, recursively, also have payload and the vertex
        # itself has a payload

        dag.a.payload = "vert-a payload (can be anything)"
        dag.d.payload = "vert-d payload (can be anything)"
        assert not dag.a.is_resolved()
        assert dag.d.is_resolved()
        assert not dag.c.is_resolved()
        dag.c.payload = "vert-c payload (can be anything)"
        dag.e.payload = "vert-d payload (can be anything)"
        assert dag.c.is_resolved()


if __name__ == '__main__':
    unittest.main()
