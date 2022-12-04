def quick_sort(a):
    if len(a) <= 1:
        return a

    pivot = a[0]
    lower = []
    greater = []

    for num in a[1:]:
        if num < pivot:
            lower.append(num)
        else:
            greater.append(num)

    return quick_sort(lower) + [pivot] + quick_sort(greater)
