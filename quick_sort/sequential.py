def quick_sort(a, l, h):
    if h - l <= 0:
        return

    p = partition(a, l, h)

    quick_sort(a, l, p)
    quick_sort(a, p + 1, h)


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
