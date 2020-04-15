import csv
import pathlib
from enum import EnumMeta


class КолонеПогрешнаВеличинаГрешка(ValueError):
    pass


class КолонеИменаСеНеПоклапајуГрешка(ValueError):
    pass


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


def учитај(путања, Тип):
    """ враћа листу редова """
    assert isinstance(путања, pathlib.Path), путања
    assert isinstance(Тип, type), Тип
    редови = []
    with путања.open('r', newline='') as ф:
        tsv = csv.reader(ф, delimiter='\t')
        for и, ред in enumerate(tsv, 1):
            if len(Тип._fields) != len(ред):
                порука = f'[{путања}][ЛИНИЈА: {и}] очекивано: {len(Тип)}, нађено: {len(ред)}'
                raise КолонеПогрешнаВеличинаГрешка(порука)
            if и == 1:
                заглавље = ред
                for и, колона in enumerate(Тип._fields):
                    if колона.upper() != заглавље[и]:
                        порука = f'[{путања}]ЗАГЛАВЉА_СЕ_НЕ_ПОКЛАПАЈУ: {колона} != {заглавље[и]}'
                        raise КолонеИменаСеНеПоклапајуГрешка(порука)
            else:
                редови.append(Тип(*ред))
    return редови


def препиши_фајл(путања, колоне, редови):
    assert isinstance(путања, pathlib.Path), путања
    assert isinstance(колоне, EnumMeta), колоне
    with путања.open('w', newline='') as ф:
        tsv = csv.writer(ф, delimiter='\t', lineterminator='\n')
        tsv.writerow([к.name for к in колоне])
        for и, ред in enumerate(редови, 1):
            if len(колоне) != len(ред):
                raise КолонеПогрешнаВеличинаГрешка(f'[{путања}][ЛИНИЈА: {и}] очекивано: {len(колоне)}, нађено: {len(ред)}')
            tsv.writerow(ред)


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
