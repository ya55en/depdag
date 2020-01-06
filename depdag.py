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

__version_tuple__ = (0, 4, 1)
__version__ = '.'.join(map(str, __version_tuple__))

from collections import OrderedDict
from typing import List, Dict, Iterable, Hashable, Union, Callable, Any

VertexName = Hashable
PayloadT = Union[object, Callable[[], bool]]


def names_only(vertices: Iterable[Vertex]) -> Iterable[VertexName]:
    """Return a generator of vertices names of given iterable sequence of vertices."""
    return (vertex.name for vertex in vertices)


def names_list(vertices: Iterable[Vertex]) -> List[VertexName]:
    """Return a list of names of given iterable sequence of vertices."""
    return list(names_only(vertices))


class Vertex:
    """A named vertices in the DAG which knows its supporters (these are
    the vertices it depends on directly), the name-to-vertices mapping object
    and its provision state (provided or not).
    """

    def __init__(self, name: VertexName, vertices_map: DepDag, payload: Any = None):
        self._name: VertexName = name
        self._vertices_map: DepDag = vertices_map
        self._supporters: OrderedDict = OrderedDict()
        self.payload: PayloadT = payload

    def __call__(self, *args, **kwargs):
        """Provide proper error in case a misspelled ``DepDag`` method is called.
        (Without this, one gets "TypeError: 'Vertex' object is not callable.)
        """
        raise AttributeError(f"Vertex object has no attribute {self._name!r}")

    def __repr__(self) -> str:
        return f"<Vertex(name={self._name!r}) object at 0x{id(self):x})>"

    @property
    def name(self) -> VertexName:
        return self._name

    def has_payload(self) -> bool:
        if self.payload is None:
            return False
        if callable(self.payload):
            return self.payload()
        return True

    def depends_on(self, *vertices: VertexName) -> None:
        """Define a dependency relationship within the DAG. If any of the vertices
        does not exist, it is created first.
        """
        self._supporters.update(OrderedDict(
            (vert, self._vertices_map[vert]) for vert in vertices
        ))

    def all_supporters(self) -> Iterable[Vertex]:
        """Return a generator iterating over all supporters of this vertices,
        retrieved recursively, debt-first, left-to-right.
        """
        for supporter in self._supporters.values():
            yield supporter

        for vert in self._supporters.values():
            for supporter in vert.all_supporters():
                yield supporter

    def direct_supporters(self) -> Iterable[Vertex]:
        """Return an iterable of supporters directly related to this vertices."""
        return self._supporters.values()

    def is_resolved(self):
        return self.has_payload() and all(
            vertex.is_resolved() for vertex in self._supporters.values()
        )


class DepDag:
    """DAG based dependency tracking main class.

    A dict-like collection of Vertices. Maps vertices names to corresponding
    ``Vertex`` objects. Creates a ``Vertex`` under given name on first access
    (if not there yet).

    Will not accept ``__setattr__`` or ``__setitem__`` assignments for vertices
    creation -- just access the not-yet-created vertices and you have it, or
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

            if not vertex.direct_supporters() or vertex in safe_vertices:
                safe_vertices |= visited_vertices
                return False

            visited_vertices.add(vertex)
            return any(check(supporter, visited_vertices.copy())
                       for supporter in vertex.direct_supporters())

        return any(check(vertex, set()) for vertex in self.all())
