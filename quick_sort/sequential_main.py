
import sys
import os
from random import randint
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(base_dir)
from wustl_cse_549_project.quick_sort import sequential

if __name__ == '__main__':

    exp = int(sys.argv[1])
    input_size = 2**exp
    a = [randint(0, input_size) for x in range(0, input_size)]

    sequential_sorted_a = sequential.quick_sort(a)