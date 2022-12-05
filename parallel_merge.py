from __future__ import print_function
import random
import sys
import time
from contextlib import contextmanager
import multiprocessing as mp
from multiprocessing import Pool
import argparse
import math


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


def seq_merge_sort_wrapper(cls_instance, A, q):
    return cls_instance.s_merge_sort(A, q)


def merge_wrapper(cls_instance, A, B, q):
    return cls_instance.merge(A, B, q)


class MergeSort(object):
    def __init__(self, array, proc_num, core_num):
        self.items = array
        self.size = len(array)
        self.p = proc_num
        self.c = core_num
        bitsize = int(math.log2(proc_num))
        self.proc_names = []
        for i in range(proc_num):
            name = "{0:b}".format(i)
            name = name.zfill(bitsize)
            self.proc_names.append(name)

    def sort(self):
        arr_size = len(self.items)
        step = arr_size // self.p
        manager = mp.Manager()
        q = manager.list()
        pool = Pool(self.c)
        if arr_size == 0:
            return []
        for i in range(len(self.proc_names)):
            bottom = i * step
            top = (i + 1) * step
            pool.apply_async(seq_merge_sort_wrapper, args=(self, self.items[bottom:top], q))
        pool.close()
        pool.join()
        proc_num = self.p // 2
        while proc_num > 0:
            pool = Pool(self.c)
            for proc in range(proc_num):
                A = q[0]
                del q[0]
                B = q[0]
                del q[0]
                pool.apply_async(merge_wrapper, args=(self, A, B, q))
            pool.close()
            pool.join()
            step *= 2
            proc_num = proc_num // 2

        answer = q[0]
        del q[0]
        return answer

    def merge(self, A, B, q):
        size = len(A)
        C = []  # List to be populated with values from A and B
        j, k = 0, 0
        for i in range(size * 2):
            if A[j] < B[k]:
                C.append(A[j])
                j += 1
                if j == size:
                    C += B[k:]
                    break
            else:
                C.append(B[k])
                k += 1
                if k == size:
                    C += A[j:]
                    break
        q.append(C)

    def s_merge_sort(self, A, q):
        if len(A) <= 1:
            if self.size == self.p:
                q.append(A)
            return A
        left = self.s_merge_sort(A[:len(A) // 2], q)
        right = self.s_merge_sort(A[len(A) // 2:], q)
        A = self.s_merge(left, right)
        a = self.size / self.p
        if len(A) == int(a):
            q.append(A)
        return A

    def s_merge(self, A, B):
        size = len(A)
        C = []
        j, k = 0, 0
        for i in range(size * 2):
            if A[j] < B[k]:
                C.append(A[j])
                j += 1
                if j == size:
                    C += B[k:]
                    break
            else:
                C.append(B[k])
                k += 1
                if k == size:
                    C += A[j:]
                    break
        return C




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge_Sort')
    parser.add_argument('--core', default='8', help='The number of workers')
    parser.add_argument('--process', default='8', help='The number of workers')
    parser.add_argument('--size', default='8', help='The number of processes')
    args = parser.parse_args()
    final_args = {"core": args.core,
                  "process": args.process,
                  "size": args.size}
    core_num = final_args["core"]
    proc_num = final_args["process"]
    size = int(final_args["size"])
    core_num = int(core_num)
    proc_num = int(proc_num)

    length = 2**size
    randomized_array = [random.randint(0, length) for i in range(length)]
    data_sorted2 = MergeSort(randomized_array, proc_num, core_num).sort()
    for i in range(len(data_sorted2) -1):
        assert data_sorted2[i] <= data_sorted2[i+1]
    assert len(data_sorted2) == length

