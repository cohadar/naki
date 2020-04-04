import csv
import pathlib
from enum import EnumMeta


class КолонеПогрешнаВеличинаГрешка(ValueError):
    pass


class КолонеИменаСеНеПоклапајуГрешка(ValueError):
    pass


def учитај_фајл(путања, колоне):
    """ враћа листу редова """
    assert isinstance(путања, pathlib.Path)
    assert isinstance(колоне, EnumMeta)
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
    assert isinstance(путања, pathlib.Path)
    assert isinstance(колоне, EnumMeta)
    with путања.open('w', newline='') as ф:
        tsv = csv.writer(ф, delimiter='\t', lineterminator='\n')
        tsv.writerow([к.name for к in колоне])
        for и, ред in enumerate(редови, 1):
            if len(колоне) != len(ред):
                raise КолонеПогрешнаВеличинаГрешка(f'[{путања}][ЛИНИЈА: {и}] очекивано: {len(колоне)}, нађено: {len(ред)}')
            tsv.writerow(ред)


def додај_на_фајл(путања, колоне, редови):
    assert isinstance(путања, pathlib.Path)
    assert isinstance(колоне, EnumMeta)
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


def _нађи(стари_редови, ред):
    for стари in стари_редови:
        if стари[0] == ред[0]:
            return (стари[0], стари[1])
    return (None, None)


def ажурирај_фајл(путања, колоне, редови):
    """ УПОЗОРЕЊЕ: Претпоставка је да су прве две колоне ид и датум """
    # TODO: тестови ѕа ово
    if путања.exists():
        стари_редови = учитај_фајл(путања, колоне)
        for ред in редови:
            ид, датум = _нађи(стари_редови, ред)
            if ид:
                ред[0], ред[1] = ид, датум
    препиши_фајл(путања, колоне, редови)
