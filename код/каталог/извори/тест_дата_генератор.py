import time
import uuid
import random
from enum import IntEnum, unique
from наки.карте import направи_карте


@unique
class Извор(IntEnum):
    ИД = 0
    ДАТУМ = 1
    ПРЕДЊА = 2
    ЗАДЊА = 3


def направи_линк(извор):
    ид = извор[Извор.ИД]
    питање = 'ли' + str(random.random())[2:]
    return [ид, f"https://www.google.de/search?tbm=isch&q={питање}"]


def извор_одради(лепа_путања, извор):
    карте = []
    индекс = iter(range(16))

    # 0, 1
    def питање(џ):
        return 'пи' + str(random.random())[2:]

    def одговор(џ):
        return 'од' + str(random.random())[2:]

    for и in range(1, random.randint(1, 16)):
        карте.extend(направи_карте(лепа_путања, извор, f"ТИП{и}", питање, одговор, next(индекс)))
    линкови = [направи_линк(и) for и in извор]
    return карте, линкови


def _рандом_датум():
    пет_година = 60*60*24*365*5
    данас = time.mktime(time.localtime())
    датум = time.localtime(данас - random.randint(0, пет_година))
    return time.strftime("%Y-%m-%d", датум)


def извор_учитај(путања):
    рез = []
    for _ in range(random.randint(50, 100)):
        рез.append([
            uuid.uuid4().hex[:-1] + '0',
            _рандом_датум(),
            'ле' + str(random.random())[2:],
            'де' + str(random.random())[2:],
        ])
    return рез
