# Distributed under the MIT license.
# Copyright (c) 2020 Yassen Damyanov and contributors
# See LICENSE and CREDITS for details.

"""
DAG-based dependency tracking utility.

Helps track dependencies via representing dependency relationships
as edges in a Directed Acyclic Graph (DAG).

For details and usage example see ``depdag`` README.rst:
  https://github.com/yassen-itlabs/depdag/blob/master/README.rst

"""

from __future__ import annotations

__version_tuple__ = (0, 3, 1)
__version__ = '.'.join(map(str, __version_tuple__))

from collections import OrderedDict
from typing import List, Dict, Iterable, Hashable, Any

VertexName = Hashable


class Vertex:
    """A named vertex in the DAG which knows its supporters (these are
    the vertices it depends on directly), the name-to-vertex mapping object
    and its provision state (provided or not).
    """

    def __init__(self, name: VertexName, vertices_map: DepDag, payload: Any = None):
        self._name: VertexName = name
        self._vertices_map: DepDag = vertices_map
        self._supporters: OrderedDict = OrderedDict()
        self.payload: Any = payload

    def __call__(self, *args, **kwargs):
        """Provide proper error in case a misspelled ``DepDag`` method is called.
        Without this one, one gets "TypeError: 'Vertex' object is not callable.
        """
        raise AttributeError(f"Vertex object has no attribute {self._name!r}")

    def __repr__(self) -> str:
        return f"<Vertex(name={self._name!r}) object at 0x{id(self):x})>"

    @property
    def name(self) -> VertexName:
        return self._name

    @property
    def is_provided(self) -> bool:
        return self.payload is not None

    def depends_on(self, *vertices: VertexName) -> None:
        self._supporters.update(OrderedDict(
            (vert, self._vertices_map[vert]) for vert in vertices
        ))

    def supporters(self, recurse: bool) -> List[VertexName]:
        if recurse:
            # gather all supporters, recursively:
            return list(self._supporters.keys()) + [
                name
                for vert in self._supporters.values()
                for name in vert.supporters(recurse=True)
            ]
        # return direct supporters of this vertex only:
        return list(self._supporters.keys())

    def direct_supporters_obj(self) -> List[Vertex]:
        return list(self._supporters.values())

    def is_resolved(self):
        return self.is_provided and all(
            vertex.is_resolved() for vertex in self._supporters.values()
        )


class DepDag:
    """DAG based dependency tracking main class.

    A dict-like collection of Vertices. Maps vertex names to corresponding
    ``Vertex`` objects. Creates a ``Vertex`` under given name on first access
    (if not there yet).

    Will not accept ``__setattr__`` or ``__setitem__`` assignments for vertex
    creation -- just access the not-yet-created vertex and you have it, or
    use the ``create()`` method.
    """

    __slots__ = ('_vertices',)

    def __init__(self):
        self._vertices: Dict[VertexName, Vertex] = dict()

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

    def is_cyclic(self) -> bool:
        """Return ``True`` if this directed graph contains at least one cycle,
        ``False`` otherwise."""

        safe_vertices = set()

        def check(vertex, visited_vertices):
            nonlocal safe_vertices

            if vertex in visited_vertices:
                return True

            if not vertex.direct_supporters_obj() or vertex in safe_vertices:
                safe_vertices |= visited_vertices
                return False

            visited_vertices.add(vertex)
            return any(check(supporter, visited_vertices.copy())
                       for supporter in vertex.direct_supporters_obj())

        return any(check(node, set()) for node in self.all())
