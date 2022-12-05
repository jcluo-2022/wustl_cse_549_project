import argparse
import random
import math
import multiprocessing as mp
from multiprocessing import Pool
import time


def seq_bitonic_sort_wrapper(cls_instance, A, order, q):
    return cls_instance.seq_bitonic_sort(A, order, q)


def merge_wrapper(cls_instance, A, B, q):
    return cls_instance.merge(A, B, q)


class BitonicSort(object):
    def __init__(self, array, up, proc_num, core_num):
        # self.func = func
        self.items = array
        self.size = len(array)
        self.order = up
        self.p = proc_num
        self.c = core_num
        # self._pool = Pool(core_num)
        bitsize = int(math.log2(proc_num))
        self.proc_names = []
        for i in range(proc_num):
            name = "{0:b}".format(i)
            name = name.zfill(bitsize)
            self.proc_names.append(name)

    def sort(self):
        arr_size = len(self.items)
        slice_size = arr_size // self.p
        manager = mp.Manager()
        # queue = manager.Queue()
        # lock = manager.Lock()
        q = manager.list()
        pool = Pool(self.c)

        if arr_size == 0:
            return []
        # Spawn all necessary processors running merge sequentially on
        # different slices
        for i in range(len(self.proc_names)):
            bottom = i * slice_size
            top = (i + 1) * slice_size
            pool.apply_async(seq_bitonic_sort_wrapper, args=(self, self.items[bottom:top], self.order, q,))
        print('Waiting for all subprocesses done...')
        pool.close()
        pool.join()
        print('All subprocesses done.')
        # print("232323",q)
        # Merges the results from each individual process
        proc_num = self.p // 2
        while proc_num > 0:
            pool = Pool(self.c)
            for proc in range(proc_num):
                A = q[0]

                del q[0]
                B = q[0]
                del q[0]
                pool.apply_async(merge_wrapper, args=(self, A, B, q,))
            print('Waiting for all subprocesses done...')
            pool.close()
            pool.join()
            print('All subprocesses done.')
            slice_size *= 2
            proc_num = proc_num // 2

        answer = q[0]
        del q[0]
        return answer

    def merge(self, A, B, q):
        size = len(A)
        C = []  # List to be populated with values from A and B
        j, k = 0, 0
        for i in range(size * 2):
            if (A[j] < B[k]) == self.order:
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

    def seq_bitonic_sort(self, A, up, q):
        if len(A) <= 1:
            if self.size == self.p:
                q.append(A)
            return A
        else:
            left = self.seq_bitonic_sort(A[:len(A) // 2], True, q)
            right = self.seq_bitonic_sort(A[len(A) // 2:], False, q)
            A = self.seq_merge(left + right, up)
            if len(A) == self.size / self.p:
                print(len(A))
                q.append(A)
            return A

    def seq_merge(self, A, up):
        """
        Sequential implementation of merge. Ran by each processor on their
        array slice.

        Args:
            A: array to be merged

        Returns:
            A merged array from two partitions
        """
        if len(A) == 1:
            return A
        else:
            self.compare(A, up)
            left = self.seq_merge(A[:len(A) // 2], up)
            right = self.seq_merge(A[len(A) // 2:], up)
            return left + right

    def compare(self, A, up):
        dist = len(A) // 2
        for i in range(dist):
            if (A[i] > A[i + dist]) == up:
                A[i], A[i + dist] = A[i + dist], A[i]


def is_ordered(A):
    size = len(A)
    for i in range(size - 1):
        if A[i] > A[i + 1]:
            return False
    return True

def compAndSwap(a, i, j, dire):
    if (dire == 1 and a[i] > a[j]) or (dire == 0 and a[i] < a[j]):
        a[i], a[j] = a[j], a[i]

def bitonicMerge(a, low, cnt, dire):
    if cnt > 1:
        k = int(cnt / 2)
        for i in range(low, low + k):
            compAndSwap(a, i, i + k, dire)
        bitonicMerge(a, low, k, dire)
        bitonicMerge(a, low + k, k, dire)


def bitonicSort(a, low, cnt, dire):
    if cnt > 1:
        k = int(cnt / 2)
        bitonicSort(a, low, k, 1)
        bitonicSort(a, low + k, k, 0)
        bitonicMerge(a, low, cnt, dire)

def sort(a, N, up):
    bitonicSort(a, 0, N, up)



def main():
    print("start")
    parser = argparse.ArgumentParser(description='Bitonic_Sort')
    parser.add_argument('--kernel_number', default='8', help='The number of workers')
    parser.add_argument('--proc_number', default='8', help='The number of processes')
    parser.add_argument('--input_size', default='20', help='The length of input list')
    args = parser.parse_args()
    final_args = {"kernel_number": args.kernel_number,
                  "proc_number": args.proc_number,
                  "input_size": args.input_size}

    s = final_args["input_size"]
    core_num = final_args["kernel_number"]
    proc_num = final_args["proc_number"]
    s = int(float(s))
    core_num = int(float(core_num))
    proc_num = int(float(proc_num))
    n = 2 ** s
    # inputSize.append(str(n))
    A = [random.randint(0, 100) for i in range(n)]
    Q = BitonicSort(A, True, proc_num, core_num)
    print(Q.sort())

if __name__ == "__main__":
    main()
