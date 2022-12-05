from __future__ import print_function
import random
import sys
import time
from contextlib import contextmanager
from multiprocessing import Manager, Pool
import argparse

def sqe_merge(*args):
    left, right = args[0] if len(args) == 1 else args
    left_length, right_length = len(left), len(right)
    left_index, right_index = 0, 0
    merged = []
    while left_index < left_length and right_index < right_length:
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    if left_index == left_length:
        merged.extend(right[right_index:])
    else:
        merged.extend(left[left_index:])
    return merged


def sqe_merge_sort(data):
    length = len(data)
    if length <= 1:
        return data
    middle = int(length / 2)
    left = sqe_merge_sort(data[:middle])
    right = sqe_merge_sort(data[middle:])
    return sqe_merge(left, right)


def merge_sort_multiple(results, array):
    results.append(merge_sort(array))


def merge_multiple(results, array_part_left, array_part_right):
    results.append(merge(array_part_left, array_part_right))


def merge_sort(array):
    array_length = len(array)

    if array_length <= 1:
        return array

    middle_index = int(array_length / 2)
    left = array[0:middle_index]
    right = array[middle_index:]
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)


def merge(left, right):
    sorted_list = []
    left = left[:]
    right = right[:]
    while len(left) > 0 or len(right) > 0:
        if len(left) > 0 and len(right) > 0:
            if left[0] <= right[0]:
                sorted_list.append(left.pop(0))
            else:
                sorted_list.append(right.pop(0))
        elif len(left) > 0:
            sorted_list.append(left.pop(0))
        elif len(right) > 0:
            sorted_list.append(right.pop(0))
    return sorted_list

# @contextmanager
# def process_pool(size):
#     pool = Pool(size)
#     yield pool
#     pool.close()
#     pool.join()


def parallel_merge_sort(array, p):
    step = int(length / p)
    manager = Manager()
    results = manager.list()

    pool = Pool(p)
    for n in range(p):
        if n < p - 1:
            chunk = array[n * step : (n + 1) * step]
        else:
            # Get the remaining elements in the list
            chunk = array[n * step:]
        pool.apply_async(merge_sort_multiple, (results, chunk))
    pool.close()
    pool.join()


    proc = p//2
    while proc >= 2:
        pool = Pool(p)
        for i in range(proc):
            pool.apply_async(merge_multiple, (results, results.pop(0), results.pop(0)))
        pool.close()
        pool.join()
        proc = proc // 2

    # proc_num = p//2
    # while proc_num > 0:
    #     pool = Pool(p)
    #     for proc in range(proc_num):
    #         pool.apply_async(merge_multiple, (results, results.pop(0), results.pop(0)))
    #         print('Waiting for all subprocesses done...')
    #     pool.close()
    #     pool.join()
    #     print('All subprocesses done.')
    #     step *= 2
    #     proc_num = proc_num // 2

    final_sorted_list = results[0]
    return final_sorted_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge_Sort')
    parser.add_argument('--proc_number', default='16', help='The number of processes')
    args = parser.parse_args()
    final_args = {"proc_number": args.proc_number}
    process_count = int(final_args['proc_number'])
    size = [2 ** 20, 2 ** 21, 2 ** 22, 2 ** 23, 2 ** 24]
    for i in range(len(size)):
        # Randomize the length of our list
        length = size[i]

        # Create an unsorted list with random numbers
        randomized_array = [random.randint(0, length) for i in range(length)]
        print('List length: {}'.format(length))
        # Create a copy first due to mutation
        start1 = time.perf_counter()
        data_sorted1 = sqe_merge_sort(randomized_array)
        T1 = time.perf_counter() - start1
        print("sequential running time is", T1)
        # print('Starting parallel sort.')
        start2 = time.perf_counter()
        data_sorted2 = parallel_merge_sort(randomized_array, process_count)
        Tp = time.perf_counter() - start2
        print("parallel running time is", Tp)
        print("Tp/T1 is ", Tp/T1)
        # print(data_sorted2)