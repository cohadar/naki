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


def направи_листу_вежбања(кв, кш):
    вежбања = [кв.вежбање(шпил=шпил) for шпил in кш.листа_шпилова()]
    вежбања.sort(key=lambda в: len(в))
    return вежбања


шк = containers.DynamicContainer()
шк.путања_каталога = providers.Object(Path('каталог'))
шк.т_интервала = providers.Factory(ТабелаИнтервала, путања=None)
шк.т_карти = providers.Factory(ТабелаКарти, путања=None)
шк.т_линкова = providers.Factory(ТабелаЛинкова, путања=None)
шк.т_записа = providers.Factory(ТабелаЗаписа, путања=None)
шк.п_интервала = providers.Factory(ПогледИнтервала, табела=шк.т_интервала)
шк.п_карти = providers.Factory(ПогледКарти, табела=шк.т_карти)
шк.п_линкова = providers.Factory(ПогледЛинкова, табела=шк.т_линкова)
шк.п_записа = providers.Factory(ПогледЗаписа, табела=шк.т_записа)
шк.шпил = providers.Factory(Шпил)
шк.листа_дирова = providers.Callable(направи_листу_дирова, шк.путања_каталога)
шк.листа_шпилова = providers.Callable(направи_листу_шпилова, контејнер=шк)

гк = containers.DynamicContainer()
гк.вежбање = providers.Factory(Вежбање, путања_каталога=шк.путања_каталога, шпил=шк.шпил)
гк.листа_вежбања = providers.Callable(направи_листу_вежбања, кв=гк, кш=шк)
гк.терминал = providers.Factory(Терминал)
гк.ui = providers.Factory(UI, терминал=гк.терминал)
гк.главна = providers.Factory(Главна, ui=гк.ui, вежбања=гк.листа_вежбања)


def main():
    print(гк.главна())


if __name__ == '__main__':
    main()

