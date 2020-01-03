"""
setuptools setup.py for depdag.

Draw inspiration from
  https://github.com/pypa/sampleproject/blob/master/setup.py ;)
"""

from setuptools import setup

setup(
    name='depdag',
    version='0.2.1',  # TODO: read it from elsewhere (e.g. separate text or .py file)
    description='A DAG-based dependency tracking utility',
    long_description='''
    A DAG-based dependency tracking utility which helps track dependencies with
    representing dependency relationships as edges in a Directed Acyclic Graph.
    ''',
    url='https://github.com/yassen-itlabs/depdag',
    author='Yassen Damyanov',
    author_email='<yassen.damyanov.bg -AT- gmail.com>',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='dependency dag',
    packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    python_requires='>=3.7, <4',
    tests_require=[],
    setup_requires=[],
    dependency_links=[],
    entry_points={},
)
