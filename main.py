import datetime
import sys

import constant.constant as constant
import quick_sort.sequential
import quick_sort.parallel
from wustl_cse_549_project.input.generate_input import generate_input

if __name__ == '__main__':

    exponent = sys.argv[1]
    generate_input(exponent)
    file_name = str(exponent) + ".txt"
    print(exponent)
    with open("./input/" + file_name, "r") as file:
        a = []
        for line in file.readlines():
            a.append(int(line))
    start_time = datetime.datetime.now()
    sequential_sorted_a = quick_sort.sequential.quick_sort(a)
    end_time = datetime.datetime.now()
    elapsed_sec = (end_time - start_time).total_seconds()
    print("sequential quick sort costs" + "{:.10f}".format(elapsed_sec) + " second")

    start_time = datetime.datetime.now()

    parallel_sorted_a = quick_sort.parallel.quick_sort(a)
    end_time = datetime.datetime.now()
    elapsed_sec = (end_time - start_time).total_seconds()
    print("parallel quick sort costs" + "{:.10f}".format(elapsed_sec) + " second")

    for j in range(0, len(parallel_sorted_a) - 1):
        assert parallel_sorted_a[j] <= parallel_sorted_a[j+1]
    print("parallel sort success.")
    print()
