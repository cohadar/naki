import time
from наки import tsv
from наки.ид import assert_ид
from datetime import date
from enum import unique, IntEnum
from collections import namedtuple, Counter
from наки.интервали import ИнтервалиЕнум


@unique
class ЗаписЕнум(IntEnum):
    КАРТА_ИД = 0
    ДАТУМ_ПРЕГЛЕДА = 1
    ВРЕМЕ_ПРЕГЛЕДА = 2
    РЕЗУЛТАТ_ПРЕГЛЕДА = 3
    НОВИ_ИНТЕРВАЛ = 4


# TODO: if unused delete
Запис2 = namedtuple('Запис', [
    'карта_ид',
    'датум_прегледа',
    'време_прегледа',
    'резултат_прегледа',
    'нови_интервал'
])


class ТабелаЗаписа():
    def __init__(бре, путања):
        бре._путања = путања
        бре._редови = []

    def учитај(бре):
        бре._редови = tsv.учитај_фајл(бре._путања, ЗаписЕнум) if бре._путања.exists() else []

    def __len__(бре):
        return len(бре._редови)

    def __iter__(бре):
        return iter(бре._редови)

    def додај(бре, редови):
        бре._редови.extend(редови)
        tsv.додај_на_фајл(бре._путања, ЗаписЕнум, редови)


class ПогледЗаписа():
    def __init__(бре, табела):
        бре._табела = табела
        бре._последња_оцена = {}
        бре._нови_интервал = Counter()
        бре._датум_прегледа = {}
        бре._табела.учитај()
        for з in бре._табела:
            ид = з[ЗаписЕнум.КАРТА_ИД]
            assert_ид(ид)
            оцена = int(з[ЗаписЕнум.РЕЗУЛТАТ_ПРЕГЛЕДА])
            бре._последња_оцена[ид] = оцена
            if оцена > 0:
                бре._нови_интервал[ид] = int(з[ЗаписЕнум.НОВИ_ИНТЕРВАЛ])
                бре._датум_прегледа[ид] = date.fromisoformat(з[ЗаписЕнум.ДАТУМ_ПРЕГЛЕДА])

    def датум_прегледа(бре, ид):
        давно = date.fromisoformat('1970-01-01')
        return бре._датум_прегледа.get(ид, давно)

    def индекс_интервала(бре, ид):
        return бре._нови_интервал[ид] - 1

    def додај_нови_интервал(бре, ид, оцена, макс_интервал):
        бре._нови_интервал[ид] = min(бре._нови_интервал[ид] + оцена, макс_интервал)
        ред = [
            ид,
            time.strftime('%Y-%m-%d'),
            time.strftime('%H:%M:%S%z'),
            оцена,
            бре._нови_интервал[ид],
        ]
        бре._табела.додај([ред])

    def промашена(бре, ид):
        return бре._последња_оцена.get(ид, 10000) > 0

    def стат_скуп_идјева(бре):
        return set(з[ЗаписЕнум.КАРТА_ИД] for з in бре._табела)

    def стат_број_карти_по_интервалу(бре):
        задњи_интервали = {}
        for за in бре._табела:
            задњи_интервали[за[ЗаписЕнум.КАРТА_ИД]] = int(за[ЗаписЕнум.НОВИ_ИНТЕРВАЛ])
        рез = [0] * len(ИнтервалиЕнум)
        for _, зи in задњи_интервали.items():
            рез[зи] += 1
        return рез

    def стат_проценат_промашених_карти(бре):
        пром = len([за for за in бре._табела if int(за[ЗаписЕнум.РЕЗУЛТАТ_ПРЕГЛЕДА]) == 0])
        return int(100 * пром / len(бре._табела))

