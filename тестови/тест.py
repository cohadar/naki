import time
import uuid
import random
from pathlib import Path
from contextlib import contextmanager
from blessings import Terminal
from наки.карте import направи_карте


class СировиТерминал():
    def __init__(бре, команде):
        assert type(команде) == list
        for к in команде:
            assert type(к) == str
        бре._и = iter(команде)
        бре._т = Terminal()
        бре.height = 48
        бре.width = 170
        бре.измене = []
        бре.отварања = []
        бре.звукова = 0

    @contextmanager
    def location(бре, x, y):
        try:
            yield 'trla baba lan'
        finally:
            pass

    def print(бре, *args, **kw):
        pass

    def input(бре, *args):
        return next(бре._и)

    def readkey(бре, *args):
        return next(бре._и)

    def clear(бре):
        pass

    def __getattr__(бре, атрибут):
        if атрибут in ['color', 'normal', 'green', 'bold', 'blue']:
            рез = getattr(бре._т, атрибут)
            if рез is None:
                raise ValueError(f'nesme none {атрибут}')
            return рез
        raise AttributeError(атрибут)

    def измени(бре, путања, линија):
        бре.измене.append((str(путања), линија))

    def отвори_урл(бре, урл):
        бре.отварања.append(урл)

    def звук_грешке(бре):
        бре.звукова += 1


def шпил_лоадер(дир, лен):
    дир = Path(дир)
    карте = []
    линкови = []
    for извор_фајл in ['aaa.tsv', 'bbb.tsv', 'ccc.tsv']:
        лепа_путања = дир.joinpath('извор', извор_фајл)
        извор = извор_учитај(извор_фајл)
        к, л = извор_одради(лепа_путања, извор)
        карте.extend(к)
        линкови.extend(л)
    интервали = [
        ["ДАТУМ", "И1", "И2", "И3", "И4", "И5", "И6", "И7", "И8", "И9"],
        ["2019-12-07", "1", "6", "15", "38", "94", "234", "586", "1465", "3662"],
        ["2019-12-07", "1", "6", "15", "38", "94", "234", "586", "1465", "3662"],
    ]
    карте = карте[:лен]
    линкови = линкови[:лен]

    def додај_запис(ред):
        pass

    return {
        "име": дир.name,
        "интервали": интервали,
        "карте": карте,
        "линкови": линкови,
        "запис": [],
        "додај_запис": додај_запис,
    }


def направи_линк(извор):
    ид = извор[0]
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

    for и in range(1, 12):
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
    for _ in range(10):
        рез.append([
            uuid.uuid4().hex[:-1] + '0',
            _рандом_датум(),
            'ле' + str(random.random())[2:],
            'де' + str(random.random())[2:],
        ])
    return рез
