from multiprocessing import Manager, Process

from wustl_cse_549_project.quick_sort import sequential


def quick_sort(a):
    with Manager() as manager:
        result = manager.list()
        quick_sort_helper(a, result)
        result = list(result)
    return result


def quick_sort_helper(a, result):
    with Manager() as manager:
        if len(a) <= 2 ** 20:
            result = manager.list(sequential.quick_sort(a))
            return

    pivot = a[0]
    lower = []
    greater = []

    for num in a[1:]:
        if num <= pivot:
            lower.append(num)
        else:
            greater.append(num)

    with Manager() as manager:
        result1 = manager.list()
        result2 = manager.list()

        p1 = Process(target=quick_sort_helper, args=(lower, result1, ))
        p2 = Process(target=quick_sort_helper, args=(greater, result2, ))

        p1.start()
        p2.start()
        p1.join()
        p2.join()
        result1.append(pivot)
        result1.extend(result2)
        result = result1

    return
