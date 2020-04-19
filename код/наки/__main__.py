from наки.конфигурација import ПУТАЊА_КАТАЛОГА
from наки.вежбање import Вежбање
from наки.шпил import Шпил
from наки.главна import Главна
from наки.терминал import Терминал
from наки.ui import UI
from наки.интервали import ПогледИнтервала, ТабелаИнтервала
from наки.запис import ПогледЗаписа, ТабелаЗаписа
from наки.линкови import ПогледЛинкова, ТабелаЛинкова
from наки.карте import ПогледКарти, ТабелаКарти
from наки import tsv


class ВежбањеЗидар():
    def __init__(бре, ui, каталог, дир):
        бре.ui = ui
        бре.каталог = каталог
        бре.дир = дир

    def __call__(бре):
        return бре.вежбање()

    def вежбање(бре):
        return Вежбање(бре.ui, бре.каталог, бре.шпил())

    def шпил(бре):
        return Шпил(
            бре.дир.name,
            бре.п_интервала(бре.дир.joinpath('интервали.tsv')),
            бре.п_карти(бре.дир.joinpath('карте.tsv')),
            бре.п_линкова(бре.дир.joinpath('линкови.tsv')),
            бре.п_записа(бре.дир.joinpath('запис.tsv')))

    def п_интервала(бре, путања):
        return ПогледИнтервала(бре.т_интервала(путања))

    def п_карти(бре, путања):
        return ПогледКарти(бре.т_карти(путања))

    def п_линкова(бре, путања):
        return ПогледЛинкова(бре.т_линкова(путања))

    def п_записа(бре, путања):
        return ПогледЗаписа(бре.т_записа(путања))

    def т_интервала(бре, путања):
        return ТабелаИнтервала(бре.tsv(), путања)

    def т_карти(бре, путања):
        return ТабелаКарти(бре.tsv(), путања)

    def т_линкова(бре, путања):
        return ТабелаЛинкова(бре.tsv(), путања)

    def т_записа(бре, путања):
        return ТабелаЗаписа(путања)

    def tsv(бре):
        return tsv


class ГлавнаЗидар():
    def __init__(бре, каталог):
        бре.каталог = каталог

    def дирови(бре):
        return [фајл for фајл in бре.каталог.iterdir() if фајл.is_dir() and not фајл.name.startswith('__')]

    def __call__(бре):
        return бре.главна()

    def главна(бре):
        return Главна(бре.ui(), бре.листа_вежбања())

    def ui(бре):
        return UI(бре.терминал())

    def терминал(бре):
        return Терминал()

    def листа_зидара_вежбања(бре):
        return [ВежбањеЗидар(бре.ui(), бре.каталог, дир) for дир in бре.дирови()]

    def листа_вежбања(бре):
        return [зв() for зв in бре.листа_зидара_вежбања()]


def главна():
    ГлавнаЗидар(ПУТАЊА_КАТАЛОГА)()()


if __name__ == '__main__':
    главна()

