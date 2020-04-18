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


def направи_листу_дирова(каталог):
    return [фајл for фајл in каталог.iterdir() if фајл.is_dir() and not фајл.name.startswith('__')]


def направи_листу_шпилова(контејнер):
    return [контејнер.шпил(
                име,
                п_интервала=контејнер.п_интервала(),
                п_карти=контејнер.п_карти(),
                п_линкова=контејнер.п_линкова(),
                п_записа=контејнер.п_записа())
            for име in контејнер.листа_дирова()]


def направи_листу_вежбања(контејнер):
    вежбања = [контејнер.вежбање(шпил=шпил) for шпил in контејнер.листа_шпилова()]
    вежбања.sort(key=lambda в: len(в))
    return вежбања


гк = containers.DynamicContainer()

гк.т_интервала = providers.Factory(ТабелаИнтервала, путања=None)
гк.т_карти = providers.Factory(ТабелаКарти, путања=None)
гк.т_линкова = providers.Factory(ТабелаЛинкова, путања=None)
гк.т_записа = providers.Factory(ТабелаЗаписа, путања=None)
гк.п_интервала = providers.Factory(ПогледИнтервала, табела=гк.т_интервала)
гк.п_карти = providers.Factory(ПогледКарти, табела=гк.т_карти)
гк.п_линкова = providers.Factory(ПогледЛинкова, табела=гк.т_линкова)
гк.п_записа = providers.Factory(ПогледЗаписа, табела=гк.т_записа)
гк.шпил = providers.Factory(Шпил)
гк.путања_каталога = providers.Object(Path('каталог'))
гк.вежбање = providers.Factory(Вежбање, путања_каталога=гк.путања_каталога, шпил=гк.шпил)
гк.листа_дирова = providers.Callable(направи_листу_дирова, гк.путања_каталога)
гк.листа_шпилова = providers.Callable(направи_листу_шпилова, контејнер=гк)
гк.листа_вежбања = providers.Callable(направи_листу_вежбања, контејнер=гк)
гк.терминал = providers.Factory(Терминал)
гк.ui = providers.Factory(UI, терминал=гк.терминал)
гк.главна = providers.Factory(Главна, ui=гк.ui, вежбања=гк.листа_вежбања)


def main():
    print(гк.главна())


if __name__ == '__main__':
    main()

