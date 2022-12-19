import random
import sys
from multiprocessing.sharedctypes import RawArray


def partition(a):
    if len(a) <= 1:
        return a
    pivot = a[0]
    lower = []
    greater = []
    for num in a[1:]:
        if num <= pivot:
            lower.append(num)
        else:
            greater.append(num)

    return lower + [pivot] + greater


if __name__ == '__main__':
    exp = int(sys.argv[1])
    input_size = 2**exp
    a = [random.randint(1, input_size) for i in range(input_size)]
    a = partition(a)
