def sequentialSearch(target, list):
    for i in range(len(list)):
        if list[i] == target:
            return i
    return -1