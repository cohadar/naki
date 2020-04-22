from наки import tsv
from collections import namedtuple


Извор = namedtuple('Извор', ['ид', 'датум', 'германски', 'превод'])


def извор_одради(кг):
    карте = []
    карте.extend(кг("ПРЕВОД <= ГЕРМАНСКИ", Извор.германски.fget, Извор.превод.fget))
    карте.extend(кг("ГЕРМАНСКИ <= ПРЕВОД", Извор.превод.fget, Извор.германски.fget))
    return карте, []


def извор_учитај(путања):
    return tsv.Табела(путања, tsv.namedtuple(Извор)).учитај()

