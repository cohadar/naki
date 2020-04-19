from наки import tsv
from enum import IntEnum, unique
from каталог.__main__ import направи_карте


@unique
class Извор(IntEnum):
    ИД = 0
    ДАТУМ = 1
    ПИТАЊЕ = 2
    ОДГОВОР = 3


def извор_одради(лепа_путања, извор):
    карте = []
    индекс = iter(range(16))

    # 0
    def питање(џ):
        return џ[Извор.ПИТАЊЕ]

    def одговор(џ):
        return џ[Извор.ОДГОВОР]

    карте.extend(направи_карте(лепа_путања, извор, "ОДГОВОР <= ПИТАЊЕ", питање, одговор, next(индекс)))
    return карте, []


def извор_учитај(путања):
    return tsv.учитај_фајл(путања, Извор)
