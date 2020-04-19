from наки import tsv
from каталог.__main__ import направи_карте
from collections import namedtuple


Извор = namedtuple('Извор', ['ид', 'датум', 'питање', 'одговор'])


def извор_одради(лепа_путања, извор):
    карте = []
    индекс = iter(range(16))
    карте.extend(направи_карте(лепа_путања, извор, "ОДГОВОР <= ПИТАЊЕ", Извор.питање.fget, Извор.одговор.fget, next(индекс)))
    return карте, []


def извор_учитај(путања):
    return tsv.учитај(путања, tsv.namedtuple(Извор))
