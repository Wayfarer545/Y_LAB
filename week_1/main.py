import itertools
from itertools import combinations
import math
import copy
from ipaddress import IPv4Address

from datetime import datetime

## первое задание
def domain_name(url: str) -> str:
    raw = url.split('.')
    if raw[0].startswith("www"):
        domain = raw[1]
    elif raw[0].startswith("http"):
        if raw[0].endswith("www"):
            domain = raw[1]
        else:
            raw = raw[0].split('//')
            domain = raw[1]
    else:
        domain = raw[0]
    return domain

## второе задание
def int32_to_ip(int32: int) -> str:
    return str(IPv4Address(int32))

## третье задание
def zeros(n) -> int:
    def zeros(n: int) -> int:
        zeros = 0
        expo = 5
        while n >= i:
            zeros += n // expo
            expo *= 5
        return zeros

## четвёртое задание
def bananas(s: str) -> set:
    result = set()
    for combination in combinations(range(len(s)), len(s)-6):
        raw = list(s)
        for i in combination:
            raw[i] = '-'
        raw = ''.join(raw)
        if raw.replace('-', '') == 'banana':
            result.add(raw)
    return result

## пятое задание
def count_find_num(primesL: list, limit: int) -> list:
    counter = 0
    largest = 0
    for n in range(2, limit + 1):
        divisor = 2
        local_list = []
        while divisor <= math.sqrt(n):
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

## тесты
def first_test():
    assert domain_name("http://google.com") == "google"
    assert domain_name("http://google.co.jp") == "google"
    assert domain_name("www.xakep.ru") == "xakep"
    assert domain_name("https://youtube.com") == "youtube"

def second_test():
    assert int32_to_ip(2154959208) == "128.114.17.104"
    assert int32_to_ip(0) == "0.0.0.0"
    assert int32_to_ip(2149583361) == "128.32.10.1"

def third_test():
    assert zeros(0) == 0
    assert zeros(6) == 1
    assert zeros(30) == 7

def fourth_test():
    assert bananas("banann") == set()
    assert bananas("banana") == {"banana"}
    assert bananas("bbananana") == {"b-an--ana", "-banana--", "-b--anana", "b-a--nana", "-banan--a",
                                    "b-ana--na", "b---anana", "-bana--na", "-ba--nana", "b-anan--a",
                                    "-ban--ana", "b-anana--"}
    assert bananas("bananaaa") == {"banan-a-", "banana--", "banan--a"}
    assert bananas("bananana") == {"ban--ana", "ba--nana", "bana--na", "b--anana", "banana--", "banan--a"}

def fifth_test():
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

if __name__ == "__main__":
    # start = datetime.now()
    # print(datetime.now() - start)
    first_test()
    second_test()
    third_test()
    fourth_test()
    fifth_test()