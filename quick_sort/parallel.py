from multiprocessing import shared_memory, Process

from wustl_cse_549_project.quick_sort import sequential
from wustl_cse_549_project.quick_sort.No_Deamon_Pool import NestablePool
from wustl_cse_549_project.quick_sort.sequential import partition


def quick_sort(a, i, j):
    if j - i <= 2 ** 18:
        sequential.quick_sort(a, i, j)
        return

    p = partition(a, i, j)
    p1 = Process(target=quick_sort, args=(a, i, p,))
    p2 = Process(target=quick_sort, args=(a, p+1, j,))
    p1.start()
    p2.start()
