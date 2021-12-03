def _index(i, n, k):
    return i * (n // k) + min(i, n % k)

def n_chunks(lst, k):
    n = len(lst)
    for i in range(k):
        yield lst[_index(i, n, k):_index(i + 1, n, k)]

def chunk(lst, k):
    for i in range(0, len(lst), k):
        yield lst[i:i + k]
