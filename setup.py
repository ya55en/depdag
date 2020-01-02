from setuptools import setup, find_packages

setup(
    name='depdag',
    version='0.2.0',
    description='A DAG-based dependency tracking utility',
    long_description='''
    Helps track dependencies via representing dependency relationships as edges in
    a Directed Acyclic Graph.
    ''',
    url='https://github.com/yassen-itlabs/depdag',
    author='Yassen Damyanov',
    author_email='<yassen.damyanov.bg -AT- gmail.com>',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='dependency dag',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    tests_require=[],
    setup_requires=[],
    dependency_links=[],
    entry_points={},
)
