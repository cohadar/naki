import time
import uuid
import random
from pathlib import Path
from hashlib import sha256
from contextlib import contextmanager
from наки.карте import направи_карте, КартаЕнум
from наки.__main__ import ГлавнаЗидар, ВежбањеЗидар


def фајл_хеш(path1):
    with open(path1, 'r') as ф:
        садржај = ф.read()
        м = sha256()
        м.update(bytes(садржај, 'utf-8'))
        return м.hexdigest()


class ТестВежбањеЗидар(ВежбањеЗидар):
    def __init__(бре, ui, каталог, дир, лен):
        super().__init__(ui, каталог, дир)
        бре.шпил_лоадер(дир, лен)

    def шпил_лоадер(бре, дир, лен):
        дир = Path(дир)
        карте = []
        линкови = []
        for извор_фајл in ['aaa.tsv', 'bbb.tsv', 'ccc.tsv']:
            лепа_путања = дир.joinpath('извор', извор_фајл)
            извор = извор_учитај(извор_фајл)
            к, л = извор_одради(лепа_путања, извор)
            карте.extend(к)
            линкови.extend(л)
        карте = карте[:лен]
        скуп_врста_карте = set()
        for карта in карте:
            скуп_врста_карте.add(карта[КартаЕнум.ВРСТА_КАРТЕ])
        интервали = []
        for врста_карте in скуп_врста_карте:
            интервали.append([врста_карте, "2019-12-07", "1", "6", "15", "38", "94", "234", "586", "1465", "3662"])
        линкови = линкови[:лен]
        запис = []
        for и, карта in enumerate(карте):
            if и % 4 == 0:
                запис.append([карта[0], "2020-03-28", "3:34:53+0100", "0", "1"])
            # TODO dodaj pregledane danas, isto kao cetvrtinu

        бре.м = {}
        бре.интервали = интервали
        бре.карте = карте
        бре.линкови = линкови
        бре.запис = запис

    def т_интервала(бре, путања):
        return ТестТабела(путања, бре.интервали)

    def т_карти(бре, путања):
        return ТестТабела(путања, бре.карте)

    def т_линкова(бре, путања):
        return ТестТабела(путања, бре.линкови)

    def т_записа(бре, путања):
        return ТестТабела(путања, бре.запис)


class ТестГлавнаЗидар(ГлавнаЗидар):
    def __init__(бре, каталог, команде, дужине):
        # super().__init__(каталог)
        бре.каталог = каталог
        бре.команде = команде
        бре.дужине = дужине
        бре.дирови = [каталог.joinpath('meh', str(и)) for и, _ in enumerate(дужине)]

    def терминал(бре):
        return ТестТерминал(бре.команде)

    def листа_вежбања(бре):
        return [ТестВежбањеЗидар(бре.ui(), бре.каталог, дир, лен)() for (дир, лен) in zip(бре.дирови, бре.дужине)]


class ТестТерминал():
    def __init__(бре, команде):
        assert type(команде) == list
        for к in команде:
            assert type(к) == str
        бре._и = iter(команде)
        бре.измене = []
        бре.отварања = []
        бре.звукова = 0
        бре._болд = '[bold]'
        бре._плаво = '[blue]'
        бре._нормал = '[/normal]'

    @contextmanager
    def статус(бре):
        try:
            yield 'статус'
        finally:
            pass

    @contextmanager
    def главни(бре):
        try:
            yield 'главни'
        finally:
            pass

    @contextmanager
    def пун_екран(бре):
        try:
            yield 'пун_екран'
        finally:
            pass

    @contextmanager
    def сакривен_курсор(бре):
        try:
            yield 'сакривен_курсор'
        finally:
            pass

    def инпут(бре, текст):
        return next(бре._и)

    def инпут_код(бре):
        return next(бре._и)

    def формат_мд(бре, текст):
        return текст

    def обриши(бре):
        pass

    def принт(бре, *args, **kw):
        pass

    def принт_сиво(бре, текст):
        pass

    def принт_плаво(бре, текст):
        pass

    def принт_зелено(бре, текст):
        pass

    def отвори_урл(бре, урл):
        бре.отварања.append(урл)

    def измени(бре, права_путања, линија):
        бре.измене.append((права_путања, линија))

    def додај_на_извор(бре, путања):
        pass

    def звук_грешке(бре):
        бре.звукова += 1


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


class ТестТабела():
    def __init__(бре, путања, на_диску):
        бре._путања = путања
        бре._редови = []
        бре._на_диску = на_диску

    def учитај(бре):
        бре._редови = []
        бре._редови.extend(бре._на_диску)

    def __len__(бре):
        return len(бре._редови)

    def __iter__(бре):
        return iter(бре._редови)

    def додај(бре, редови):
        бре._редови.extend(редови)
        бре._на_диску.extend(редови)

