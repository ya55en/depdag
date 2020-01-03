
depdag
======

A DAG-based dependency tracking utility


Disclaimer
**********

This library is largely provided as-is. It is in early state
of development and breaking changes may happen without warning.


Intro
*****

Helps track dependencies via representing dependency relationships as edges in
a Directed Acyclic Graph (DAG). We call a vertex depending on other vertices
a *dependant*, and a vertex other vertices depend on a *supporter*.

In case entities represented by DAG vertices may have certain payload associated
with them, depdag provides answer to the question: "Is this vertex resolved?",
that is, has it and all its supporters, recursively, been provided with payload
-- the ``Vertex::is_resolved()`` method does that.


An example
**********

An example of typical usage:

.. code:: python

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


Running the tests
*****************

Using the standard library `unittest` would do::

 $ python -m unittest -discover ./tests/

or with recent versions of python3, simply::

 $ python -m unittest

If you have (or are willing to install) `pytest`, it would also work fine::

 $ pytest ./tests/




Local install & PR strategy
***************************
Note for when the repo is installed via pip install -e <repo dir> so that the library can be imported
in projects but also can be changed inplace. In order to make a PR for a change to this repo, a branch in a fork is needed.
Proposed strategy
* clone locally & install this package via pip install -e
* add as a git remote the address of the forked repo `git remote add forked <url of fork repo>`
* when a change is done locally, put it on a feature branch and push it to the fork so that a PR can be opened
* once the PR is approved, locally, checkout master & pull