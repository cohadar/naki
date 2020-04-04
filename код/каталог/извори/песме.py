from наки.карте import направи_карте
from enum import IntEnum, unique


@unique
class Извор(IntEnum):
    ИД = 0
    ДАТУМ = 1
    НАСЛОВ = 2
    СТРОФА1 = 3
    СТРОФА2 = 4


def направи_линк(извор):
    ид = извор[Извор.ИД]
    питање = извор[Извор.НАСЛОВ]
    return [ид, f"https://soundcloud.com/search?q={питање}"]


def извор_одради(лепа_путања, извор):
    карте = []
    индекс = iter(range(16))

    # 0
    def питање(џ):
        return џ[Извор.СТРОФА1]

    def одговор(џ):
        return џ[Извор.СТРОФА2]

    for и, строфе in enumerate(извор):
        карте.extend(направи_карте(лепа_путања, [строфе], f"СТРОФА {и}", питање, одговор, next(индекс)))

    линкови = [направи_линк(и) for и in извор]
    return карте, линкови


def извор_учитај(путања):
    with open(путања, 'r') as ф:
        линије = [линија.strip() for линија in ф.readlines()]
    ид, датум = линије[0].split('\t')
    линије = линије[1:]
    песма = []
    строфа = []
    for линија in линије:
        if линија:
            строфа.append(линија)
        else:
            песма.append(строфа)
            строфа = []
    if строфа:
        песма.append(строфа)
    песма = ['\\n'.join(строфа) for строфа in песма]
    return [[ид, датум, линије[0], строфа1, строфа2] for строфа1, строфа2 in zip(песма[:-1], песма[1:])]
