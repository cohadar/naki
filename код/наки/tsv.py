import csv
import pathlib
from enum import EnumMeta


class ЗаглављеГрешка(ValueError):
    pass


class ПарсирањеГрешка(ValueError):
    pass


class КолонеПогрешнаВеличинаГрешка(ValueError):
    pass


class КолонеИменаСеНеПоклапајуГрешка(ValueError):
    pass


def учитај(путања, неко):
    """ учитај фајл и парсирај елементе """
    assert isinstance(путања, pathlib.Path), путања
    with путања.open('r', newline='') as ф:
        tsv = csv.reader(ф, delimiter='\t')
        for и, ред in enumerate(tsv, 1):
            if и == 1:
                заг = неко.заглавље()
                if ред != заг:
                    raise ЗаглављеГрешка(f"Заглавље се не поклапа: {заг} {ред}")
            else:
                try:
                    неко.append(неко.елемент(ред))
                except Exception as е:
                    raise ПарсирањеГрешка(f'(линија:{и}){ред}', е)


def додај(путања, неко, елементи):
    assert isinstance(путања, pathlib.Path), путања
    """ додај елементе на крај фајла """
    додај_заглавље = False
    if путања.exists():
        with путања.open('r', newline='') as ф:
            tsv = csv.reader(ф, delimiter='\t')
            ред = next(tsv)
            заг = неко.заглавље()
            if ред != заг:
                raise ЗаглављеГрешка(f"Заглавље се не поклапа: {заг} {ред}")
    else:
        додај_заглавље = True
    with путања.open('a', newline='') as ф:
        tsv = csv.writer(ф, delimiter='\t', lineterminator='\n')
        if додај_заглавље:
            tsv.writerow(неко.заглавље())
        for елемент in елементи:
            tsv.writerow(неко.ред(елемент))


def учитај_фајл(путања, колоне):
    """ враћа листу редова """
    assert isinstance(путања, pathlib.Path), путања
    assert isinstance(колоне, EnumMeta), колоне
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
    assert isinstance(путања, pathlib.Path), путања
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

