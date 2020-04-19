from datetime import date
from collections import namedtuple


БРОЈ_ИНТЕРВАЛА = 9


Интервали = namedtuple('Интервали', ['врста_карте', 'датум', 'интервали'])


class ТабелаИнтервала():
    def __init__(бре, tsv, путања):
        бре._tsv = tsv
        бре._путања = путања
        бре._елементи = []

    def учитај(бре):
        бре._елементи.extend(бре._tsv.учитај(бре._путања, бре))
        for е in бре._елементи:
            assert isinstance(е, Интервали)

    def додај(бре, елементи):
        бре._елементи.extend(елементи)
        бре._tsv.додај(бре._путања, бре, елементи)
        for е in бре._елементи:
            assert isinstance(е, Интервали)

    def __len__(бре):
        return len(бре._елементи)

    def __iter__(бре):
        return iter(бре._елементи)

    def заглавље(бре):
        return [п.upper() for п in Интервали._fields]

    def ред(бре, елемент):
        return [елемент[0], елемент[1].isoformat(), ', '.join(str(е) for е in елемент[2])]

    def елемент(бре, ред):
        ив = [int(и.strip()) for и in ред[2].split(',')]
        assert all(а < б for (а, б) in zip(ив[:-1], ив[1:]))
        return Интервали(ред[0], date.fromisoformat(ред[1]), ив)


class ПогледИнтервала():
    def __init__(бре, табела):
        бре._табела = табела
        бре._табела.учитај()
        бре._интервали = [и for и in бре._табела]
        бре._интервали.sort(key=lambda и: и.датум, reverse=True)

    @staticmethod
    def предефинисани_интервали(врста_карте):
        return Интервали(
            врста_карте,
            date.today(),
            [1, 6, 15, 38, 94, 234, 586, 1465, 3662]
        )

    def има_врсту_карте(бре, врста_карте):
        for ив in бре._интервали:
            if ив.врста_карте == врста_карте:
                return True
        return False

    def консолидуј(бре, скуп_врста_карте):
        assert isinstance(скуп_врста_карте, set)
        нови_интервали = []
        for врста_карте in скуп_врста_карте:
            if not бре.има_врсту_карте(врста_карте):
                и = бре.предефинисани_интервали(врста_карте)
                нови_интервали.append(и)
                бре._интервали.append(и)
        if нови_интервали:
            бре._табела.додај(нови_интервали)
        бре._интервали.sort(key=lambda и: и.датум, reverse=True)
        assert len(бре._табела) == len(бре._интервали)

    def период_интервала(бре, врста_карте, индекс_интервала):
        for и in бре._интервали:
            if и.врста_карте == врста_карте:
                return и.интервали[индекс_интервала]
        raise KeyError(f'период_интервала(врста_карте="{врста_карте}", индекс_интервала="{индекс_интервала}")')

    def __len__(бре):
        return len(бре._интервали)

