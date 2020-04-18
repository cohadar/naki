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


def направи_листу_шпилова():
    return [Container.ф_шпил(
                име,
                п_интервала=Container.ф_п_интервала(),
                п_карти=Container.ф_п_карти(),
                п_линкова=Container.ф_п_линкова(),
                п_записа=Container.ф_п_записа())
            for име in Container.ф_листа_дирова()]


def направи_листу_вежбања():
    вежбања = [Container.ф_вежбање(шпил=шпил) for шпил in Container.ф_листа_шпилова()]
    вежбања.sort(key=lambda в: len(в))
    return вежбања


class Container(containers.DeclarativeContainer):
    ф_т_интервала = providers.Factory(ТабелаИнтервала, путања=None)
    ф_т_карти = providers.Factory(ТабелаКарти, путања=None)
    ф_т_линкова = providers.Factory(ТабелаЛинкова, путања=None)
    ф_т_записа = providers.Factory(ТабелаЗаписа, путања=None)

    ф_п_интервала = providers.Factory(ПогледИнтервала, табела=ф_т_интервала)
    ф_п_карти = providers.Factory(ПогледКарти, табела=ф_т_карти)
    ф_п_линкова = providers.Factory(ПогледЛинкова, табела=ф_т_линкова)
    ф_п_записа = providers.Factory(ПогледЗаписа, табела=ф_т_записа)

    ф_шпил = providers.Factory(Шпил)
    ф_путања_каталога = providers.Object(Path('каталог'))
    ф_вежбање = providers.Factory(Вежбање, путања_каталога=ф_путања_каталога, шпил=ф_шпил)
    ф_листа_дирова = providers.Callable(направи_листу_дирова, ф_путања_каталога)
    ф_листа_шпилова = providers.Callable(направи_листу_шпилова)
    ф_листа_вежбања = providers.Callable(направи_листу_вежбања)
    ф_терминал = providers.Factory(Терминал)
    ф_ui = providers.Factory(UI, терминал=ф_терминал)
    ф_главна = providers.Factory(Главна, ui=ф_ui, вежбања=ф_листа_вежбања)


def main():
    print(Container.ф_главна())


if __name__ == '__main__':
    main()
