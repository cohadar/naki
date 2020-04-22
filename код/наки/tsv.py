import csv
from pathlib import Path


class ЗаглављеГрешка(ValueError):
    pass


class ПарсирањеГрешка(ValueError):
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
    def __init__(бре, путања, Тип):
        бре._путања = путања
        бре._Тип = Тип
        бре._елементи = []

    def учитај(бре):
        бре._елементи.clear()
        бре._елементи.extend(бре._учитај(бре._путања, бре._Тип))
        return бре

    def додај(бре, елементи):
        бре._елементи.extend(елементи)
        бре._додај(бре._путања, бре._Тип, елементи)

    def __len__(бре):
        return len(бре._елементи)

    def __iter__(бре):
        return iter(бре._елементи)

    def _учитај(бре, путања, Тип):
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
                        raise ПарсирањеГрешка(f'(линија:{и}){ред}') from е
            return елементи

    def _додај(бре, путања, Тип, елементи):
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

