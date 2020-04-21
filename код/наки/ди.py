from наки.конфигурација import ПУТАЊА_КАТАЛОГА
from pathlib import Path
from collections import namedtuple
import dependency_injector.containers as containers
import dependency_injector.providers as providers


Табела = namedtuple('Табела', ['путања', 'Тип'])

ПогледИнтервала = namedtuple('ПогледИнтервала', ['табела'])
ПогледКарти = namedtuple('ПогледКарти', ['табела'])
ПогледЛинкова = namedtuple('ПогледЛинкова', ['табела'])
ПогледЗаписа = namedtuple('ПогледЗаписа', ['табела'])

Шпил = namedtuple('Шпил', ['дир', 'п_интервала', 'п_карти', 'п_линкова', 'п_записа'])
Вежбање = namedtuple('Вежбање', ['путања_каталога', 'шпил'])
Терминал = namedtuple('Терминал', [])
UI = namedtuple('UI', ['терминал'])
Главна = namedtuple('Главна', ['ui', 'вежбања'])

ТестТерминал = namedtuple('ТестТерминал', ['команде'])
ТестТабела = namedtuple('ТестТабела', ['путања', 'Тип', 'на_диску'])


class Контејнер(containers.DynamicContainer):
    def листа_дирова(к, каталог):
        return [фајл for фајл in каталог.iterdir() if фајл.is_dir() and not фајл.name.startswith('__')]

    def листа_вежбања(к):
        рез = []
        for дир in к.дирови():
            к.дир.override(providers.Object(дир))
            рез.append(к.вежбање())
        return рез

    def __init__(к):
        super().__init__()
        к.каталог = providers.Object(ПУТАЊА_КАТАЛОГА)
        к.дирови = providers.Callable(к.листа_дирова, каталог=к.каталог)

        к.дир = providers.Object(None)
        к.путања_интервали = providers.Callable(lambda дир: дир.joinpath('интервали.tsv'), к.дир)
        к.путања_карте = providers.Callable(lambda дир: дир.joinpath('карте.tsv'), к.дир)
        к.путања_линкови = providers.Callable(lambda дир: дир.joinpath('линкови.tsv'), к.дир)
        к.путања_запис = providers.Callable(lambda дир: дир.joinpath('запис.tsv'), к.дир)

        к.т_интервала = providers.Callable(Табела, путања=к.путања_интервали, Тип='Интервали')
        к.т_карти = providers.Factory(Табела, путања=к.путања_карте, Тип='Карте')
        к.т_линкова = providers.Factory(Табела, путања=к.путања_линкови, Тип='Линкови')
        к.т_записа = providers.Factory(Табела, путања=к.путања_запис, Тип='Запис')

        к.п_интервала = providers.Factory(ПогледИнтервала, табела=к.т_интервала)
        к.п_карти = providers.Factory(ПогледКарти, табела=к.т_карти)
        к.п_линкова = providers.Factory(ПогледЛинкова, табела=к.т_линкова)
        к.п_записа = providers.Factory(ПогледЗаписа, табела=к.т_записа)

        к.шпил = providers.Factory(
            Шпил,
            дир=к.дир,
            п_интервала=к.п_интервала,
            п_карти=к.т_карти,
            п_линкова=к.т_линкова,
            п_записа=к.т_записа)

        к.вежбање = providers.Factory(Вежбање, путања_каталога=к.каталог, шпил=к.шпил)
        к.вежбања = providers.Callable(к.листа_вежбања)
        к.терминал = providers.Factory(Терминал)
        к.ui = providers.Singleton(UI, терминал=к.терминал)
        к.главна = providers.Factory(Главна, ui=к.ui, вежбања=к.вежбања)


class ТестКонтејнер(Контејнер):
    def __init__(к):
        super().__init__()
        к.терминал.override(providers.Factory(ТестТерминал, команде=[4, 5]))
        к.т_интервала.override(providers.Factory(ТестТабела, путања=к.путања_интервали, Тип='Интервали', на_диску=[1, 2]))
        к.т_карти.override(providers.Factory(ТестТабела, путања=к.путања_карте, Тип='Карте', на_диску=[1, 2]))
        к.т_линкова.override(providers.Factory(ТестТабела, путања=к.путања_линкови, Тип='Линкови', на_диску=[1, 2]))
        к.т_записа.override(providers.Factory(ТестТабела, путања=к.путања_запис, Тип='Запис', на_диску=[1, 2]))

    def листа_дирова(к, каталог):
        return [Path('aaa'), Path('bbb'), Path('ccc')]


def main():
    к = Контејнер()
    print(к.главна())
    к = ТестКонтејнер()
    print(к.главна())


if __name__ == '__main__':
    main()

