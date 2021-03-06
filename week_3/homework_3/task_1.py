import json
from functools import wraps
from redis import Redis


def decorate_em(func):
    @wraps(func)
    def wrapper(**kwargs) -> int:
        """
        Декоратор использует редис в качестве кэша для значений
        именованных аргументов и результата работы функции.
        Необходимо указать хост и порт сервера.
        """
        with Redis(
                host='127.0.0.1',
                port=6379
                ) as connection:
            stored_kwargs = connection.get('kwargs')
            if stored_kwargs and kwargs == json.loads(stored_kwargs):
                result = connection.get('result')
            else:
                result = func(**kwargs)
                connection.set('kwargs', json.dumps(kwargs))
                connection.set('result', result)
        return int(result)
    return wrapper

@decorate_em
def multiplier(number: int) -> int:
    return number * 2


if __name__ == '__main__':
    print(multiplier(number=3))