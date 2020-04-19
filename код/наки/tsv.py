import csv
from pathlib import Path
from enum import EnumMeta


class ЗаглављеГрешка(ValueError):
    pass


class ПарсирањеГрешка(ValueError):
    pass


class КолонеПогрешнаВеличинаГрешка(ValueError):
    pass


class КолонеИменаСеНеПоклапајуГрешка(ValueError):
    pass


def namedtuple(Тип):
    """ украшава namedtuple Тип sa atributima potrebnim za tsv серијалиѕацију """
    def заглавље():
        return [п.upper() for п in Тип._fields]

    def ред(елемент):
        return list(елемент)

    def елемент(ред):
        return Тип(*ред)

    setattr(Тип, 'заглавље', заглавље)
    setattr(Тип, 'ред', ред)
    setattr(Тип, 'елемент', елемент)
    return Тип


class Табела():
    def __init__(бре, tsv, путања, Тип):
        бре._tsv = tsv
        бре._путања = путања
        бре._Тип = Тип
        бре._елементи = []

    def учитај(бре):
        бре._елементи.extend(бре._tsv.учитај(бре._путања, бре._Тип))

    def додај(бре, елементи):
        бре._елементи.extend(елементи)
        бре._tsv.додај(бре._путања, бре._Тип, елементи)

    def __len__(бре):
        return len(бре._елементи)

    def __iter__(бре):
        return iter(бре._елементи)


def учитај(путања, Тип):
    """ учитај фајл и парсирај елементе """
    assert isinstance(путања, Path), путања
    if not путања.exists():
        return []
    with путања.open('r', newline='') as ф:
        tsv = csv.reader(ф, delimiter='\t')
        елементи = []
        for и, ред in enumerate(tsv, 1):
            if и == 1:
                заг = Тип.заглавље()
                if ред != заг:
                    raise ЗаглављеГрешка(f"Заглавље се не поклапа: {заг} {ред}")
            else:
                try:
                    елементи.append(Тип.елемент(ред))
                except Exception as е:
                    raise ПарсирањеГрешка(f'(линија:{и}){ред}', е)
        return елементи


def додај(путања, Тип, елементи):
    assert isinstance(путања, Path), путања
    """ додај елементе на крај фајла """
    додај_заглавље = False
    if путања.exists():
        with путања.open('r', newline='') as ф:
            tsv = csv.reader(ф, delimiter='\t')
            ред = next(tsv)
            заг = Тип.заглавље()
            if ред != заг:
                raise ЗаглављеГрешка(f"Заглавље се не поклапа: {заг} {ред}")
    else:
        додај_заглавље = True
    with путања.open('a', newline='') as ф:
        tsv = csv.writer(ф, delimiter='\t', lineterminator='\n')
        if додај_заглавље:
            tsv.writerow(Тип.заглавље())
        for елемент in елементи:
            tsv.writerow(Тип.ред(елемент))


def учитај_фајл(путања, колоне):
    """ враћа листу редова """
    assert isinstance(путања, Path), путања
    assert isinstance(колоне, EnumMeta), колоне
    if not путања.exists():
        return []
    редови = []
    with путања.open('r', newline='') as ф:
        tsv = csv.reader(ф, delimiter='\t')
        for и, ред in enumerate(tsv, 1):
            if len(колоне) != len(ред):
                raise КолонеПогрешнаВеличинаГрешка(f'[{путања}][ЛИНИЈА: {и}] очекивано: {len(колоне)}, нађено: {len(ред)}')
            редови.append(ред)
    заглавље, редови = редови[0], редови[1:]
    for и, колона in enumerate(колоне):
        if колона.name != заглавље[и]:
            raise КолонеИменаСеНеПоклапајуГрешка(f'[{путања}]ЗАГЛАВЉА_СЕ_НЕ_ПОКЛАПАЈУ: {колона.name} != {заглавље[и]}')
    return редови


def додај_на_фајл(путања, колоне, редови):
    assert isinstance(путања, Path), путања
    assert isinstance(колоне, EnumMeta), колоне
    """ додај редове у фајл """
    додај_заглавље = False
    if путања.exists():
        with путања.open('r', newline='') as ф:
            tsv = csv.reader(ф, delimiter='\t')
            заглавље = next(tsv)
            for и, колона in enumerate(колоне):
                if колона.name != заглавље[и]:
                    raise КолонеИменаСеНеПоклапајуГрешка(f'[{путања}]ЗАГЛАВЉА_СЕ_НЕ_ПОКЛАПАЈУ: {колона.name} != {заглавље[и]}')
    else:
        додај_заглавље = True
    with путања.open('a', newline='') as ф:
        tsv = csv.writer(ф, delimiter='\t', lineterminator='\n')
        if додај_заглавље:
            tsv.writerow([к.name for к in колоне])
        for и, ред in enumerate(редови, 1):
            if len(колоне) != len(ред):
                raise КолонеПогрешнаВеличинаГрешка(f'[{путања}][ЛИНИЈА: {и}] очекивано: {len(колоне)}, нађено: {len(ред)}')
            tsv.writerow(ред)

