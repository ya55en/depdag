# Distributed under the MIT license.
# Copyright (c) 2020 Yassen Damyanov <yassen.damyanov.bg -AT- gmail.com>
# See LICENSE file for details.

"""
DAG-based dependency tracking utility.

Helps track dependencies via representing dependency relationships as edges in
a Directed Acyclic Graph (DAG). We call a vertex depending on other vertices
a *dependant*, and a vertex that other vertices depend on a *supporter*.

In case entities represented by DAG vertices may have certain payload associated
with them, depdag provides answer to the question: "Is this vertex resolved?",
that is, has it and all its supporters, recursively, being provided with payload
-- the `Vertex::is_resolved()` method does that.

Here an example of typical usage::

 from depdag import DepDag

 # Create the DAG structure and get a reference to the vertices collection:
 vert = DepDag().vertices

 # Connect vertices with directed dependency relationships (i.e. the edges):
 vert.a.depends_on('b')
 vert.b.depends_on('d')
 vert.c.depends_on('d', 'e')
 assert not vert.dag.is_cyclic()

 # Explore who depends on whom, recursively; prints:
 # - vert a -> all supporters: ['b', 'd']
 # - vert b -> all supporters: ['d']
 # - vert d -> all supporters: []
 # - vert c -> all supporters: ['d', 'e']
 # - vert e -> all supporters: []
 for v in vert.all():
     print("- vert", v.name, "-> all supporters:", v.supporters(recurse=True))

 # Set some payload and see which vertices are 'resolved', that is,
 # all supporters, recursively, also have payload and the vertex
 # itself has a payload

 vert.a.payload = "vert-a payload (can be anything)"
 vert.d.payload = "vert-d payload (can be anything)"
 assert not vert.a.is_resolved()
 assert vert.d.is_resolved()
 assert not vert.c.is_resolved()
 vert.c.payload = "vert-c payload (can be anything)"
 vert.e.payload = "vert-d payload (can be anything)"
 assert vert.c.is_resolved()

"""

from __future__ import annotations

__version_tuple__ = (0, 2, 0)
__version__ = '.'.join(map(str, __version_tuple__))

from collections import OrderedDict
from typing import List, Dict, Iterable, Optional, Any, Hashable

VertexName = Hashable


class Vertex:
    """A named vertex in the DAG which knows its supporters (these are
    the vertices it depends on directly), the name-to-vertex mapping object
    and its provision state (provided or not).
    """
    __slots__ = ('_name', '_vertices_map', '_supporters', '_provided', 'payload')

    def __init__(self, name: VertexName, vertices_map: VerticesMap):
        self._name: VertexName = name
        self._vertices_map: VerticesMap = vertices_map
        self._supporters: OrderedDict = OrderedDict()
        self.payload: Any = None

    def __repr__(self) -> str:
        return f"<Vertex(name={self._name!r}) object at 0x{id(self):x})>"

    @property
    def name(self) -> VertexName:
        return self._name

    @property
    def provided(self) -> bool:
        return self.payload is not None

    def depends_on(self, *vertices: VertexName) -> None:
        self._supporters.update(OrderedDict(
            (vert, self._vertices_map[vert]) for vert in vertices
        ))

    def supporters(self, recurse: bool) -> List[VertexName]:
        if recurse:
            # gather all supporters, recursively:
            return list(self._supporters.keys()) + [
                name for vert in self._supporters.values()
                for name in vert.supporters(recurse=True)
            ]
        # return direct supporters of this vertex only:
        return list(self._supporters.keys())

    def is_resolved(self):
        return self.provided and all(
            vertex.is_resolved() for vertex in self._supporters.values()
        )


class VerticesMap:
    __slots__ = ('_vertices', '_dag')

    def __init__(self, dag: Optional[DepDag]):
        self._vertices: Dict[VertexName, Vertex] = dict()
        self._dag = dag

    @property
    def dag(self):
        return self._dag
     
    def __contains__(self, item):
        return item in self._vertices

    def __len__(self):
        return len(self._vertices)

    def __getattr__(self, name: VertexName) -> Vertex:
        if name not in self._vertices:
            self._vertices[name] = Vertex(name, self)
        return self._vertices[name]

    def __getitem__(self, name: VertexName) -> Vertex:
        if name not in self._vertices:
            self._vertices[name] = Vertex(name, self)
        return self._vertices[name]

    def __setitem__(self, name: VertexName, value: Vertex) -> None:
        raise NotImplementedError("cannot set/assign vertices")

    def create(self, name: VertexName) -> Vertex:
        assert name not in self._vertices
        self._vertices[name] = result = Vertex(name, self)
        return result

    def all(self) -> Iterable[Vertex]:
        return self._vertices.values()


class DepDag:
    """DAG based dependency tracking utility class."""

    def __init__(self):
        self._vertices: VerticesMap = VerticesMap(self)

    @property
    def vertices(self) -> VerticesMap:
        return self._vertices

    def is_cyclic(self) -> bool:
        """Return True if this directed graph contains at least one cycle,
        False otherwise."""
        # Yes -- ugly, Q&D, expensive implementation. A better one is on the way ;)
        # TODO: provide proper implementation
        try:
            for vert in self._vertices.all():
                vert.supporters(recurse=True)
        except RecursionError:
            return True
        else:
            return False
