import csv
import pathlib
from enum import EnumMeta


class КолонеПогрешнаВеличинаГрешка(ValueError):
    pass


class КолонеИменаСеНеПоклапајуГрешка(ValueError):
    pass


class Табела():
    """ рад са tsv фајловима као редовима података """
    def __init__(бре, путања, Тип):
        assert isinstance(путања, pathlib.Path), путања
        assert isinstance(Тип, type), Тип
        бре._путања = путања
        бре._Тип = Тип
        бре._редови = []

    def учитај(бре):
        """ учитај редове из фајла """
        бре._редови = []
        with бре._путања.open('r', newline='') as ф:
            tsv = csv.reader(ф, delimiter='\t')
            for и, ред in enumerate(tsv, 1):
                if len(бре._Тип._fields) != len(ред):
                    порука = f'[{бре._путања}][ЛИНИЈА: {и}] очекивано: {len(бре._Тип._fields)}, нађено: {len(ред)}'
                    raise КолонеПогрешнаВеличинаГрешка(порука)
                if и == 1:
                    заглавље = ред
                    for и, колона in enumerate(бре._Тип._fields):
                        if колона.upper() != заглавље[и]:
                            порука = f'[{бре._путања}]ЗАГЛАВЉА_СЕ_НЕ_ПОКЛАПАЈУ: {колона.upper()} != {заглавље[и]}'
                            raise КолонеИменаСеНеПоклапајуГрешка(порука)
                else:
                    бре._редови.append(бре._Тип(*ред))
        return бре

    def препиши(бре, редови):
        """ препиши цео фајл """
        бре._редови = редови
        with бре._путања.open('w', newline='') as ф:
            tsv = csv.writer(ф, delimiter='\t', lineterminator='\n')
            tsv.writerow([к.upper() for к in бре._Тип._fields])
            for и, ред in enumerate(редови, 1):
                if len(бре._Тип._fields) != len(ред):
                    порука = f'[{бре._путања}][ЛИНИЈА: {и}] очекивано: {len(бре._Тип._fields)}, нађено: {len(ред)}'
                    raise КолонеПогрешнаВеличинаГрешка(порука)
                tsv.writerow(ред)
        return бре

    def додај(бре, редови):
        """ додај редове у фајл """
        бре._редови.extend(редови)
        додај_заглавље = False
        if бре._путања.exists():
            with бре._путања.open('r', newline='') as ф:
                tsv = csv.reader(ф, delimiter='\t')
                заглавље = next(tsv)
                for и, колона in enumerate(бре._Тип._fields):
                    if колона.upper() != заглавље[и]:
                        порука = f'[{бре._путања}]ЗАГЛАВЉА_СЕ_НЕ_ПОКЛАПАЈУ: {колона.upper()} != {заглавље[и]}'
                        raise КолонеИменаСеНеПоклапајуГрешка(порука)
        else:
            додај_заглавље = True
        with бре._путања.open('a', newline='') as ф:
            tsv = csv.writer(ф, delimiter='\t', lineterminator='\n')
            if додај_заглавље:
                tsv.writerow([к.upper() for к in бре._Тип._fields])
            for и, ред in enumerate(редови, 1):
                if len(бре._Тип._fields) != len(ред):
                    порука = f'[{бре._путања}][ЛИНИЈА: {и}] очекивано: {len(бре._Тип._fields)}, нађено: {len(ред)}'
                    raise КолонеПогрешнаВеличинаГрешка(порука)
                tsv.writerow(ред)
        return бре

    def __len__(бре):
        return len(бре._редови)

    def __iter__(бре):
        return iter(бре._редови)


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
