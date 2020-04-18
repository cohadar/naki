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


class М():
    def м_дирови(бре):
        каталог = бре.м_каталог()
        return [фајл for фајл in каталог.iterdir() if фајл.is_dir() and not фајл.name.startswith('__')]

    def м_Шпил(бре, дир):
        п_интервала = ПогледИнтервала(ТабелаИнтервала(дир.joinpath('интервали.tsv')))
        п_карти = ПогледКарти(ТабелаКарти(дир.joinpath('карте.tsv')))
        п_записа = ПогледЗаписа(ТабелаЗаписа(дир.joinpath('запис.tsv')))
        п_линкова = ПогледЛинкова(ТабелаЛинкова(дир.joinpath('линкови.tsv')))
        return Шпил(дир.name, п_интервала, п_карти, п_линкова, п_записа)

    def м_шпилови(бре):
        return [бре.м_Шпил(дир) for дир in бре.м_дирови()]

    def м_каталог(бре):
        return ПУТАЊА_КАТАЛОГА

    def м_вежбања(бре):
        вежбања = [Вежбање(бре.м_каталог(), шпил) for шпил in бре.м_шпилови()]
        вежбања.sort(key=lambda в: len(в))
        return вежбања

    def м_Терминал(бре):
        return Терминал()

    def м_UI(бре):
        return UI(бре.м_Терминал())

    def м_Главна(бре):
        return Главна(бре.м_UI(), бре.м_вежбања())


def главна():
    м = М()
    м.м_Главна()()


if __name__ == '__main__':
    главна()

