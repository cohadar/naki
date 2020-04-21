from наки.конфигурација import ПУТАЊА_КАТАЛОГА
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
ТестТабела = namedtuple('ТестТабела', ['путања', 'на_диску'])


def листа_дирова(каталог):
    return [фајл for фајл in каталог.iterdir() if фајл.is_dir() and not фајл.name.startswith('__')]


def листа_вежбања(к):
    рез = []
    for дир in к.дирови():
        к.дир.override(providers.Object(дир))
        рез.append(к.вежбање())
    return рез


def контејнер():
    к = containers.DynamicContainer()
    к.дир = providers.Object(None)
    к.каталог = providers.Object(ПУТАЊА_КАТАЛОГА)
    к.дирови = providers.Callable(листа_дирова, каталог=к.каталог)

    к.т_интервала = providers.Factory(Табела, путања=к.дир, Тип='Интервали')
    к.т_карти = providers.Factory(Табела, путања=к.дир, Тип='Карте')
    к.т_линкова = providers.Factory(Табела, путања=к.дир, Тип='Линкови')
    к.т_записа = providers.Factory(Табела, путања=к.дир, Тип='Запис')

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
    к.вежбања = providers.Callable(листа_вежбања, к)
    к.терминал = providers.Factory(Терминал)
    к.ui = providers.Singleton(UI, терминал=к.терминал)
    к.главна = providers.Factory(Главна, ui=к.ui, вежбања=к.вежбања)
    return к


def main():
    к = контејнер()
    print(к.главна())


if __name__ == '__main__':
    main()

