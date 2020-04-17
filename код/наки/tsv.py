import csv
import pathlib
from enum import EnumMeta


class КолонеПогрешнаВеличинаГрешка(ValueError):
    pass


class КолонеИменаСеНеПоклапајуГрешка(ValueError):
    pass


class Табела():
    def __init__(бре, путања, Тип):
        бре.путања = путања
        бре.Тип = Тип

    def учитај_редове(бре):
        """ враћа листу редова """
        assert isinstance(бре.путања, pathlib.Path), бре.путања
        редови = []
        with бре.путања.open('r', newline='') as ф:
            tsv = csv.reader(ф, delimiter='\t')
            for и, ред in enumerate(tsv, 1):
                if len(бре.Тип._fields) != len(ред):
                    порука = f'[{бре.путања}][ЛИНИЈА: {и}] очекивано: {len(бре.Тип)}, нађено: {len(ред)}'
                    raise КолонеПогрешнаВеличинаГрешка(порука)
                if и == 1:
                    заглавље = ред
                    for и, колона in enumerate(бре.Тип._fields):
                        if колона.upper() != заглавље[и]:
                            порука = f'[{бре.путања}]ЗАГЛАВЉА_СЕ_НЕ_ПОКЛАПАЈУ: {колона} != {заглавље[и]}'
                            raise КолонеИменаСеНеПоклапајуГрешка(порука)
                else:
                    редови.append(бре.Тип(*ред))
        return редови


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
