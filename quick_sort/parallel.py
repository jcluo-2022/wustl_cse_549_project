from wustl_cse_549_project.quick_sort import sequential
from wustl_cse_549_project.quick_sort.No_Deamon_Pool import NestablePool


def quick_sort(a):

    if len(a) <= 2 ** 18:
        return sequential.quick_sort(a)

    pivot = a[0]
    lower = []
    greater = []

    for num in a[1:]:
        if num <= pivot:
            lower.append(num)
        else:
            greater.append(num)

    pool = NestablePool()
    res1 = pool.apply_async(quick_sort, (lower, ))
    res2 = pool.apply_async(quick_sort, (greater, ))
    pool.close()
    pool.join()

    return res1.get() + [pivot] + res2.get()
