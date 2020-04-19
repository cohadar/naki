from наки import tsv
from enum import IntEnum, unique
from каталог.__main__ import направи_карте


@unique
class Извор(IntEnum):
    ИД = 0
    ДАТУМ = 1
    НОМИНАТИВ = 2
    ГЕНИТИВ = 3
    ДАТИВ = 4
    АКУЗАТИВ = 5


def извор_одради(лепа_путања, извор):
    карте = []
    индекс = iter(range(16))

    def питање(џ):
        return џ[Извор.НОМИНАТИВ]

    # 0
    def одговор(џ):
        return џ[Извор.ГЕНИТИВ]

    карте.extend(направи_карте(лепа_путања, извор, "ГЕНИТИВ <= НОМИНАТИВ", питање, одговор, next(индекс)))

    # 1
    def одговор(џ):
        return џ[Извор.ДАТИВ]

    карте.extend(направи_карте(лепа_путања, извор, "ДАТИВ <= НОМИНАТИВ", питање, одговор, next(индекс)))

    # 2
    def одговор(џ):
        return џ[Извор.АКУЗАТИВ]

    карте.extend(направи_карте(лепа_путања, извор, "АКУЗАТИВ <= НОМИНАТИВ", питање, одговор, next(индекс)))

    return карте, []


def извор_учитај(путања):
    return tsv.учитај_фајл(путања, Извор)
