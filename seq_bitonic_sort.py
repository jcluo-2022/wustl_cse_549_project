import argparse
import random
import math
import multiprocessing as mp
from multiprocessing import pool
import time
import matplotlib.pyplot as plt


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bitonic_Sort')
    parser.add_argument('--input_size', default='3', help='The length of input list')
    args = parser.parse_args()
    final_args = {"input_size": args.input_size}
    s = final_args["input_size"]
    s=int(float(s))
    n = 2 ** s
    A = [random.randint(0, 100) for i in range(n)]
    sort(A, n, 1)
    print(A)