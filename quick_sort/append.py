import random
import sys
from multiprocessing.sharedctypes import RawArray


def partition(a, l, h):
    pivot = a[(l+h)//2]
    i = l-1
    j = h+1
    while 1:

        while 1:
            i += 1
            if a[i] >= pivot:
                break

        while 1:
            j -= 1
            if a[j] <= pivot:
                break

        if i >= j:
            return j

        tmp = a[j]
        a[j] = a[i]
        a[i] = tmp


if __name__ == '__main__':
    exp = int(sys.argv[1])
    input_size = 2**exp
    a = [random.randint(1,input_size) for i in range(input_size)]
    partition(a,0,len(a)-1)
