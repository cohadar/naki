from наки import tsv
from collections import namedtuple


Извор = namedtuple('извор', ['ид', 'датум', 'links', 'rechts', 'лево', 'десно'])


def извор_одради(кг):
    карте = []

    # 0, 1
    def питање(џ):
        return f"{џ.links} und {џ.rechts}"

    def одговор(џ):
        return f"{џ.лево} i {џ.десно}"

    карте.extend(кг("ПРЕВОД <= ГЕРМАНСКИ", питање, одговор))
    карте.extend(кг("ГЕРМАНСКИ <= ПРЕВОД", одговор, питање))

    # 2, 3
    def питање(џ):
        return f"{џ.rechts} und {џ.links}"

    def одговор(џ):
        return f"{џ.десно} i {џ.лево}"

    карте.extend(кг("ПРЕВОД <= ГЕРМАНСКИ", питање, одговор))
    карте.extend(кг("ГЕРМАНСКИ <= ПРЕВОД", одговор, питање))
    return карте, []


def извор_учитај(путања):
    return tsv.Табела(путања, tsv.namedtuple(Извор)).учитај()

