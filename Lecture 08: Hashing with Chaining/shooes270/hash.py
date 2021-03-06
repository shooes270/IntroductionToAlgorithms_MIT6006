"""
Table resizing
- hash functions (div, mul, univ)

Rolling hash
Karp-Rabin algorithm (String match)
"""
import math
import random


primes = [2, 3, 5, 7, 11]


def lower_bound(n, s, e):
    while (e-s) > 0:
        mid = (s+e) // 2
        if n <= primes[mid]:
            e = mid
        else:
            s = mid+1
    return primes[s]


def get_prime_exceed(n):
    largest = primes[-1]
    if n <= largest:
        return lower_bound(n, 0, len(primes))
    for next in range(largest+2, n*2, 2):
        is_prime = True
        for p in primes:
            # if not prime
            if next % p == 0:
                is_prime = False
                break
            if next <= (p*p):
                break
        if is_prime:
            primes.append(next)
            if next >= n:
                return next

    return primes[-1]


class Div:

    def __init__(self, size=8):
        self.size = size
        self.m = get_prime_exceed(size)

    def __call__(self, key):
        return key % self.m

    def get_size(self):
        return self.m


class Mul:

    def __init__(self, size=8):
        self.size = size
        self.r = math.floor(math.log(size, 2)) # 최대 2^6개의 키값을 저장
        self.w = 32 # 64비트 환경에선 64를 사용
        self.m = int(math.pow(2, self.w))
        self.a = random.randint(self.m//2, self.m) # a는 홀수이며 구간 (2^(w-1), 2^w)에서 랜덤하게 선택
        if self.a % 2 == 0:
            if self.a-self.m//2 > self.m-self.a: # a가 2^w에 더 가까울 경우
                self.a = self.a-1
            else:
                self.a = self.a+1

    def __call__(self, key):
        return (self.a*key % self.m) >> (self.w-self.r)

    def get_size(self):
        return int(math.pow(2, self.r))


class Univ:

    def __init__(self, size=8):
        self.size = size
        self.__setup__()

    def __setup__(self):
        self.p = get_prime_exceed(self.size*2) # p는 universal size 이상의 소수
        self.a = random.randint(0, self.p-1)
        self.b = random.randint(0, self.p-1)
        self.m = get_prime_exceed(self.size)

    def __call__(self, key):
        return ((self.a*key + self.b) % self.p) % self.m

    def get_size(self):
        return self.m


class Hash:

    def __init__(self, h=Div):
        self.h = h()
        self.capacity = self.h.get_size()
        self.items = [None] * self.capacity
        self.size = 0

    def insert(self, item):
        key = self.h(item.__hash__())
        if self.items[key] is None:
            self.items[key] = [item]
        else:
            self.items[key].append(item)

    def show_table(self):
        for i in range(self.capacity):
            print('{0} - {1}'.format(i, self.items[i]))


def main():
    hash_functions = [Div, Mul, Univ]
    data = [
        'exercitation', 'incididunt', 'Lorem', 'culpa',
        'Ut', 'enim', 'veniam', 'consectetur', 'occaecat',
        'magna', 'dolore', 'do', 'minim', 'ex',
        'ipsum', 'nulla', 'qui', 'sit', 'deserunt',
        'mollit', 'ea', 'cillum', 'voluptate', 'sint',
        'dolor', 'nostrud', 'velit', 'id', 'nisi',
        'laboris', 'irure', 'est', 'labore', 'Duis',
        'proident', 'sunt', 'aliquip', 'in', 'reprehenderit',
        'eiusmod', 'Excepteur', 'ullamco', 'fugiat', 'aliqua',
        'quis', 'anim', 'amet', 'et', 'sed',
        'pariatur', 'consequat', 'esse', 'cupidatat', 'commodo',
        'eu', 'adipiscing', 'officia', 'tempor', 'elit',
        'ad', 'non', 'ut', 'aute', 'laborum'
    ]
    for func in hash_functions:
        hash = Hash(h=func)
        for word in data:
            hash.insert(word)
        hash.show_table()
        print('-'*100)


if __name__ == "__main__":
    main()