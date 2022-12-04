import argparse
import random
import math
import multiprocessing as mp
from multiprocessing import pool
import time
import matplotlib.pyplot as plt





class BitonicSort():
    def __init__(self, array, up, proc_num, core_num):
        self.items = array
        self.size = len(array)
        self.order = up
        self.p = proc_num
        self.c = core_num
        bitsize = int(math.log2(proc_num))
        self.proc_names = []
        for i in range(proc_num):
            name = "{0:b}".format(i)
            name = name.zfill(bitsize)
            self.proc_names.append(name)

    def sort(self):
        """
        Bitonic sort. Parallel sort algorithm that runs in O(log^2(n))

        Args:
            array (int[]): the list to be sorted
            up     (bool): if True list is sorted in ascending order, if False list is
                           sorted in descending order

        Returns:
            A sorted sequence of numbers.
        """
        arr_size = len(self.items)
        slice_size = arr_size // self.p
        q = mp.Queue()
        proc_arr = []

        if arr_size == 0:
            return []
        # Spawn all necessary processors running merge sequentially on
        # different slices
        j = 0
        l = 0
        for i in range(len(self.proc_names)):
            bottom = i * slice_size
            top = (i + 1) * slice_size
            p = mp.Process(target=self.seq_bitonic_sort,
                           args=(self.items[bottom:top], self.order, q),
                           name=self.proc_names[i])
            proc_arr.append(p)
            p.start()
            j += 1
            if (j == self.c or i == len(self.proc_names) - 1):
                for t in range(l, i + 1):
                    proc_arr[t].join()
                l = i + 1
                j = 0

        # Wait for processes to terminate before merging
        # for i in range(len(self.proc_names)):
        #     proc_arr[i].join()

        # Merges the results from each individual process
        proc_num = self.p // 2
        proc_arr.clear()
        j = 0
        l = 0
        while proc_num > 0:
            for proc in range(proc_num):
                A = q.get()
                B = q.get()
                p = mp.Process(target=self.merge, args=(A, B, q))
                proc_arr.append(p)
                p.start()
                j += 1
                if (j == self.c or proc == proc_num - 1):
                    for t in range(l, proc + 1):
                        proc_arr[t].join()
                    l = proc + 1
                    j = 0
            slice_size *= 2
            proc_num = proc_num // 2
            # for i in range(len(proc_arr)):
            #     proc_arr[i].join()
            proc_arr.clear()

        answer = q.get()
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

        q.put(C)

    def seq_bitonic_sort(self, A, up, q):
        if len(A) <= 1:
            if self.size == self.p:
                q.put(A)
            return A
        else:
            left = self.seq_bitonic_sort(A[:len(A) // 2], True, q)
            right = self.seq_bitonic_sort(A[len(A) // 2:], False, q)
            A = self.seq_merge(left + right, up)
            if len(A) == self.size / self.p:
                q.put(A)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bitonic_Sort')
    parser.add_argument('--kernel_number', default='8', help='The number of workers')
    parser.add_argument('--proc_number', default='8', help='The number of processes')
    parser.add_argument('--input_size', default='3', help='The length of input list')
    args = parser.parse_args()
    final_args = {"kernel_number": args.kernel_number,
                  "proc_number": args.proc_number,
                  "input_size": args.input_size}
    # resultslop=[]
    # resultSeqTime=[]
    # resultParallelTime=[]
    # inputSize=[]
    s = final_args["input_size"]
    core_num = final_args["kernel_number"]
    proc_num = final_args["proc_number"]
    s = int(s)
    core_num = int(core_num)
    proc_num = int(proc_num)
    n = 2 ** s
    # inputSize.append(str(n))
    A = [random.randint(0, 100) for i in range(n)]
    start = time.perf_counter()
    sort(A, n, 1)
    end = time.perf_counter()
    t1=end-start
    print("sequential run time is ",t1,"s")
    start=time.perf_counter()
    Q = BitonicSort(A, True, proc_num, core_num)
    end = time.perf_counter()
    print(Q.sort())
    # print(result)
    t2=end-start
    print("parallel run time is ",t2,"s")
    slop=t2/t1
    print("Tp/T1 is ",slop)

    # if(is_ordered(result)):
    #     resultSeqTime.append(t1)
    #     resultParallelTime.append(t2)
    #     resultslop.append(slop)
    # plt.plot(inputSize, resultSeqTime)
    # plt.xlabel("InputSize")
    # plt.ylabel("Time")
    # plt.title("Execution Time (Model: Sequential)")
    # plt.savefig('./Sequential time.png')
    # plt.clf()
    # plt.plot(inputSize, resultslop)
    # plt.xlabel("InputSize")
    # plt.ylabel("Tp/T1")
    # plt.title("Time Ratio (Tp/T1)")
    # plt.savefig('./Time Ratio.png')
    # plt.clf()
    # plt.plot(inputSize, resultParallelTime)
    # plt.xlabel("InputSize")
    # plt.ylabel("Time")
    # plt.title("Execution Time (Model: Parallel)")
    # plt.savefig('./Parallel time.png')
    # plt.clf()
