from наки import tsv
from collections import namedtuple


Извор = namedtuple('извор', ['ид', 'датум', 'неодређени_члан', 'једнина', 'множина', 'превод'])


def направи_линк(извор):
    питање = извор.неодређени_члан + ' ' + извор.једнина
    return [извор.ид, f"https://www.google.de/search?tbm=isch&q={питање}"]


def извор_одради(кг):
    карте = []

    def питање(џ):
        return f"d.. {џ.једнина}"

    def одговор(џ):
        return f"{џ.неодређени_члан} {џ.једнина}"

    # 0
    карте.extend(кг("ЧЛАН <= ЈЕДНИНА", питање, одговор))

    # 1, 2
    карте.extend(кг("MNOЖИНА <= ЈЕДНИНА", Извор.једнина.fget, Извор.множина.fget))
    карте.extend(кг("ЈЕДНИНА <= MNOЖИНА", Извор.множина.fget, Извор.једнина.fget))

    # 3, 4
    карте.extend(кг("PREVOD <= ЈЕДНИНА", Извор.једнина.fget, Извор.превод.fget))
    карте.extend(кг("ЈЕДНИНА <= PREVOD", Извор.превод.fget, Извор.једнина.fget))
    линкови = [направи_линк(и) for и in кг.извор]
    return карте, линкови


def извор_учитај(путања):
    return tsv.Табела(путања, tsv.namedtuple(Извор)).учитај()

