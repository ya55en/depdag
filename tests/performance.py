"""
Create large DAGs and test is_cyclic() performance.
"""

from timeit import timeit
from depdag import DepDag


def create_large_dag(nodes=1000, fail_on_cycle=False):
    dag = DepDag(fail_on_cycle=fail_on_cycle)
    for idx in range(nodes//3):
        name = f'node-{idx}'
        dag.create(name)
        dag[name].depends_on(name + '-one')
        dag[name].depends_on(name + '-two')


def perf_test():
    size = 3000
    no_cycle_check_time = timeit(lambda: create_large_dag(3000), number=1)
    cycle_check_time = timeit(lambda: create_large_dag(3000, True), number=1)

    print(f"{size}-vertices DepDag(fail_on_cycle=False):", no_cycle_check_time, 'sec.')
    print(f"{size}-vertices DepDag(fail_on_cycle=True):", cycle_check_time, 'sec.')
    print("Second is", cycle_check_time/no_cycle_check_time, "times slower.")


if __name__ == '__main__':
    perf_test()
