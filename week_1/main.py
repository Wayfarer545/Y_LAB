import itertools
import math
import copy
from ipaddress import IPv4Address


## первое задание
def domain_name(url: str) -> str:
    raw = url.split('.')
    if raw[0] == "www":
        domain = raw[1]
    else:
        raw = raw[0].split('//')
        domain = raw[1]
    return domain

assert domain_name("http://google.com") == "google"
assert domain_name("http://google.co.jp") == "google"
assert domain_name("www.xakep.ru") == "xakep"
assert domain_name("https://youtube.com") == "youtube"


## второе задание
def int32_to_ip(int32: int) -> str:
    return str(IPv4Address(int32))

assert int32_to_ip(2154959208) == "128.114.17.104"
assert int32_to_ip(0) == "0.0.0.0"
assert int32_to_ip(2149583361) == "128.32.10.1"


## третьео задание
def zeros(n: int) -> int:
    if n > 0:
        k_max = math.log(n, 5)
        z = 0
        for k in range(1, n + 1):
            z += n / (5 ** k)
    else:
        z = 0
    return int(z)

assert zeros(0) == 0
assert zeros(6) == 1
assert zeros(30) == 7


## четвёртое задание
def bananas(s: str) -> set:
    result = set()
    if len(s) >= 6:
        mask = "111111" + ("0" * (len(s) - 6))
        for i in itertools.permutations(mask):
            sample = list(s)
            for j, k in enumerate(i):
                if k == "0":
                    sample[j] = "-"
            match = ''.join(sample)
            if match.replace('-', '') == 'banana':
                result.add(match)
    return result

assert bananas("banann") == set()
assert bananas("banana") == {"banana"}
assert bananas("bbananana") == {"b-an--ana", "-banana--", "-b--anana", "b-a--nana", "-banan--a",
                                "b-ana--na", "b---anana", "-bana--na", "-ba--nana", "b-anan--a",
                                "-ban--ana", "b-anana--"}
assert bananas("bananaaa") == {"banan-a-", "banana--", "banan--a"}
assert bananas("bananana") == {"ban--ana", "ba--nana", "bana--na", "b--anana", "banana--", "banan--a"}


## пятое задание
def count_find_num(primesL: list, limit: int) -> list:
    counter = 0
    largest = 0
    for n in range(2, limit + 1):
        divisor = 2
        local_list = []
        while divisor ** 2 <= n:
            if n % divisor == 0:
                n //= divisor
                local_list.append(divisor)
            else:
                divisor += 1
        if n != 1:
            local_list.append(n)
        if set(local_list) == set(primesL):
            counter += 1
            largest = math.prod(local_list)
    if counter != 0:
        return [counter, largest]
    else:
        return []

primesL = [2, 3]
limit = 200
assert count_find_num(primesL, limit) == [13, 192]

primesL = [2, 5]
limit = 200
assert count_find_num(primesL, limit) == [8, 200]

primesL = [2, 3, 5]
limit = 500
assert count_find_num(primesL, limit) == [12, 480]

primesL = [2, 3, 5]
limit = 1000
assert count_find_num(primesL, limit) == [19, 960]

primesL = [2, 3, 47]
limit = 200
assert count_find_num(primesL, limit) == []






