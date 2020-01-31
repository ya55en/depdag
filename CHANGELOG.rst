
depdag CHANGELOG
================

Ver. 0.4.2
----------

- implement clone method (PR #15)
- provide `fail_on_cycle` option at creation (PR #13)


Ver. 0.4.1
----------
unreleased, in development

Breaking changes:

- rename ``is_provided`` to ``has_payload()``
- break ``supporters()`` into ``all_supporters()`` and ``direct_supporters()``
- introduce ``names_only()`` and ``names_list()`` helper functions

Improvements:

- proper ``is_cyclic()`` implementation
- make DepDag iterable


Ver. 0.3.1
----------
unreleased, in development


Ver. 0.2.1
----------
*Released: 2020-01-03*

Joro Tenev's improvements with PR #1:
- Provide `VerticesMap::__contains__()`
- Allow any `Hashable` to be used as ``Vertex`` names

Also,
- Provide real world test cases (Veren Damyanov's PR #2)
- Add CI via .github/workflow/pythonpackage.yml


Ver. 0.2.0
----------
*Released: 2020-01-02*

First version released to public.
