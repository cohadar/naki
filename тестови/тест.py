import time
import uuid
import random
from pathlib import Path
from contextlib import contextmanager
from blessings import Terminal
from collections import Counter
from наки.карте import направи_карте, Линк, Карта


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


class ТестШпилДиск():
    def __init__(бре, дир, лен):
        бре.дир = Path(дир)
        бре._карте = []
        бре._линкови = []
        for извор_фајл in ['aaa.tsv', 'bbb.tsv', 'ccc.tsv']:
            лепа_путања = бре.дир.joinpath('извор', извор_фајл)
            извор = извор_учитај(извор_фајл)
            к, л = извор_одради(лепа_путања, извор)
            бре._карте.extend(к)
            бре._линкови.extend(л)
        бре._карте = бре._карте[:лен]
        бре._линкови = бре._линкови[:лен]
        бре.запис_путања = Path(дир).joinpath('запис.tsv')

    def учитај_интервале(бре):
        return [1, 6, 15, 38, 94, 234, 586, 1465, 3662]

    def учитај_запис(бре):
        нови_интервал = Counter()
        датум_прегледа = {}
        последња_оцена = {}
        return (нови_интервал, датум_прегледа, последња_оцена)

    def учитај_линкове(бре):
        линк_мапа = {}
        for л in бре._линкови:
            линк_мапа[л[Линк.ИД]] = л[Линк.УРЛ]
        return линк_мапа

    def учитај_активне_карте(бре, може_данас):
        # _провера_јединствености(бре._активне)
        return [карта for карта in бре._карте if може_данас(карта[Карта.ИД])]

    def додај_запис(бре, ред):
        pass


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
