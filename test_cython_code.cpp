# ↓ -n <ファイル名>をつけることで後でファイルが確認しやすくなります。
%%cython -n test_cython_code
def fib(int n):
    cdef int i
    cdef double a=0.0, b=1.0

    for i in range(n):
        a, b = a+b, a
    return a

def primes(int kmax):
    cdef int n, k, i
    cdef int p[1000]
    result = []

    if kmax > 1000:
        kmax = 1000

    k = 0
    n = 2
    while k < kmax:
        i = 0
        while i < k and n % p[i] != 0:
            i += 1

        if i == k:
            p[k] = n
            k += 1
            result.append(n)
        n += 1
    return result

