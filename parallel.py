import argparse
import math
import multiprocessing
import random
import sys
import time

def merge(*args):
    # Support explicit left/right args, as well as a two-item
    # tuple which works more cleanly with multiprocessing.
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


def merge_sort(data):
    length = len(data)
    if length <= 1:
        return data
    middle = int(length / 2)
    left = merge_sort(data[:middle])
    right = merge_sort(data[middle:])
    return merge(left, right)

class MergeSort():
    def __init__(self, array):
        self.items = array
        self.size = len(array)
        self.p = 16
        bitsize = int(math.log2(self.p))
        self.proc_names = []
        for i in range(self.p):
            name = "{0:b}".format(i)
            name = name.zfill(bitsize)
            self.proc_names.append(name)

    def sort(self):
        print(1)
        arr_size = len(self.items)
        slice_size = arr_size//self.p
        q = multiprocessing.Queue()
        proc_arr = []

        if arr_size == 0:
            return []
        for i in range(len(self.proc_names)):
            bottom = i*slice_size
            top = (i+1)*slice_size
            p = multiprocessing.Process(target=self.seq_merge_sort,
                           args=(self.items[bottom:top], q),
                           name=self.proc_names[i])
            proc_arr.append(p)
            p.start()
        for i in range(len(self.proc_names)):
            proc_arr[i].join()

        # Merges the results from each individual process
        proc_num = self.p//2
        proc_arr.clear()
        while proc_num > 0:
            for proc in range(proc_num):
                A = q.get()
                B = q.get()
                p = multiprocessing.Process(target=self.merge, args=(A, B, q))
                proc_arr.append(p)
                p.start()
            slice_size *= 2
            proc_num = proc_num // 2
            for i in range(len(proc_arr)):
                proc_arr[i].join()
            proc_arr.clear()

        answer = q.get()
        return answer

    def merge(self, A, B, q):
        size = len(A)
        C = [] # List to be populated with values from A and B
        j, k = 0, 0
        for i in range(size*2):
            if (A[j] < B[k]):
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

        q.put(C)

    def seq_merge_sort(self, A, q):
        if len(A) <= 1:
            if self.size == self.p:
                q.put(A)
            return A
        else:
            left = self.seq_merge_sort(A[:len(A) // 2], q)
            right = self.seq_merge_sort(A[len(A) // 2:], q)
            A = self.seq_merge(left+right)
            if len(A) == self.size/self.p:
                q.put(A)
            return A

    def seq_merge(self, *args):
        left, right = args[0] if len(args) == 1 else args
        left_length, right_length = len(left), len(right)
        left_index, right_index = 0, 0
        merged = []
        while left_index_length and right_index < right_length:
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
        return merged < left


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge_Sort')
    parser.add_argument('--kernel_number', default='8', help='The number of workers')
    parser.add_argument('--proc_number', default='8', help='The number of processes')
    args = parser.parse_args()
    final_args = {"kernel_number": args.kernel_number,
                  "proc_number": args.proc_number}
    core_num = final_args["kernel_number"]
    proc_num = final_args["proc_number"]
    core_num = int(core_num)
    proc_num = int(proc_num)
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
        data_sorted2 = MergeSort(randomized_array, proc_num, core_num).sort()
        Tp = time.perf_counter() - start2
        print("parallel running time is", Tp)
        print("Tp/T1 is ", Tp / T1)
        # print(data_sorted2)
