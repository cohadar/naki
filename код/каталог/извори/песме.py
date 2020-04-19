from каталог.__main__ import направи_карте
from collections import namedtuple


Извор = namedtuple('извор', ['ид', 'датум', 'наслов', 'строфа1', 'строфа2'])


def направи_линк(ид, наслов):
    return [ид, f"https://soundcloud.com/search?q={наслов}"]


def извор_одради(лепа_путања, извор):
    карте = []
    линкови = []
    индекс = iter(range(16))

    for и, строфе in enumerate(извор):
        ка = направи_карте(лепа_путања, [строфе], f"СТРОФА {и}", Извор.строфа1.fget, Извор.строфа2.fget, next(индекс))
        линкови.extend([направи_линк(к[0], извор[0].наслов) for к in ка])
        карте.extend(ка)

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
    return [Извор(ид, датум, линије[0], строфа1, строфа2) for строфа1, строфа2 in zip(песма[:-1], песма[1:])]

