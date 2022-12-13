import random
def distribute(a):

    if (len(a)<=1):
        return a
    pivot = a[0]
    lower = []
    greater = []

    for num in a[1:]:
        if num < pivot:
            lower.append(num)
        else:
            greater.append(num)

    return lower + [pivot] + greater

if __name__ == '__main__':
    a = [random.randint(1,2**20) for i in range(2**20)]
    pivot = a[0]
    lower = []
    greater = []

    for num in a[1:]:
        if num < pivot:
            lower.append(num)
        else:
            greater.append(num)
    # b = lower + [pivot] + greater
    b = distribute(lower) + [pivot] + distribute(greater)