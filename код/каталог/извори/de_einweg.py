from наки import tsv
from collections import namedtuple


Извор = namedtuple('Извор', ['ид', 'датум', 'питање', 'одговор'])


def извор_одради(кг):
    карте = []
    карте.extend(кг("ОДГОВОР <= ПИТАЊЕ", Извор.питање.fget, Извор.одговор.fget))
    return карте, []


def извор_учитај(путања):
    return tsv.Табела(путања, tsv.namedtuple(Извор)).учитај()
