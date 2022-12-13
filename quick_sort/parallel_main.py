
import sys
import os
from multiprocessing.managers import SharedMemoryManager
from random import randint
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(base_dir)
from wustl_cse_549_project.quick_sort import parallel


if __name__ == '__main__':
    with SharedMemoryManager() as smm:
        exp = int(sys.argv[1])
        input_size = 2 ** exp

        # a = shared_memory.ShareableList([randint(0, input_size) for x in range(0, input_size)], name='a')
        a = smm.ShareableList([randint(0, input_size) for x in range(0, input_size)])
        parallel.quick_sort(a, 0, len(a)-1)
        for i in range(0, len(a) - 1):
            assert a[i] <= a[i+1]