from pathlib import Path
from collections import namedtuple
import dependency_injector.containers as containers
import dependency_injector.providers as providers


ТабелаИнтервала = namedtuple('ТабелаИнтервала', ['путања'])
ТабелаКарти = namedtuple('ТабелаКарти', ['путања'])
ТабелаЛинкова = namedtuple('ТабелаЛинкова', ['путања'])
ТабелаЗаписа = namedtuple('ТабелаЗаписа', ['путања'])

ПогледИнтервала = namedtuple('ПогледИнтервала', ['табела'])
ПогледКарти = namedtuple('ПогледКарти', ['табела'])
ПогледЛинкова = namedtuple('ПогледЛинкова', ['табела'])
ПогледЗаписа = namedtuple('ПогледЗаписа', ['табела'])

Шпил = namedtuple('Шпил', ['име', 'п_интервала', 'п_карти', 'п_линкова', 'п_записа'])
Вежбање = namedtuple('Вежбање', ['путања_каталога', 'шпил'])
Терминал = namedtuple('Терминал', [])
UI = namedtuple('UI', ['терминал'])
Главна = namedtuple('Главна', ['ui', 'вежбања'])


def контејнер_вежбања(каталог, путања):
    к = containers.DynamicContainer()
    к.т_интервала = providers.Factory(ТабелаИнтервала, путања=путања)
    к.т_карти = providers.Factory(ТабелаКарти, путања=путања)
    к.т_линкова = providers.Factory(ТабелаЛинкова, путања=путања)
    к.т_записа = providers.Factory(ТабелаЗаписа, путања=путања)
    к.п_интервала = providers.Factory(ПогледИнтервала, табела=к.т_интервала)
    к.п_карти = providers.Factory(ПогледКарти, табела=к.т_карти)
    к.п_линкова = providers.Factory(ПогледЛинкова, табела=к.т_линкова)
    к.п_записа = providers.Factory(ПогледЗаписа, табела=к.т_записа)
    к.шпил = providers.Factory(
        Шпил,
        име=путања,
        п_интервала=к.п_интервала(),
        п_карти=к.п_карти(),
        п_линкова=к.п_линкова(),
        п_записа=к.п_записа())
    к.вежбање = providers.Factory(Вежбање, путања_каталога=каталог, шпил=к.шпил)
    return к


def листа_дирова(каталог):
    return [фајл for фајл in каталог.iterdir() if фајл.is_dir() and not фајл.name.startswith('__')]


def направи_листу_вежбања(каталог):
    дирови = листа_дирова(каталог)
    лк = [контејнер_вежбања(каталог, дир) for дир in дирови]
    вежбања = [к.вежбање() for к in лк]
    вежбања.sort(key=lambda в: len(в))
    return вежбања


def контејнер_главни(каталог):
    гк = containers.DynamicContainer()
    гк.листа_вежбања = providers.Callable(направи_листу_вежбања, каталог)
    гк.терминал = providers.Factory(Терминал)
    гк.ui = providers.Factory(UI, терминал=гк.терминал)
    гк.главна = providers.Factory(Главна, ui=гк.ui, вежбања=гк.листа_вежбања)
    return гк


def main():
    каталог = Path('каталог')
    гк = контејнер_главни(каталог)
    print(гк.главна())


if __name__ == '__main__':
    main()

