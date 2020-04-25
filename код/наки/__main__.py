from наки.конфигурација import ПУТАЊА_КАТАЛОГА
from наки.шпил import Шпил
from наки.главна import Главна
from наки.главна_ui import ГлавнаUI
from наки.питање_ui import ПитањеUI
from наки.одговор_ui import ОдговорUI
from наки.терминал import Терминал
from наки.команда import Регистар
from наки.интервали import ПогледИнтервала, Интервали
from наки.запис import ПогледЗаписа, Запис
from наки.линкови import ПогледЛинкова, Линк
from наки.карте import ПогледКарти, Карта
from наки.tsv import Табела
import dependency_injector.containers as containers
import dependency_injector.providers as providers


class ШпилКонтејнер(containers.DynamicContainer):
    def __init__(к, отац, дир):
        super().__init__()
        к.отац = отац
        к.дир = providers.Object(дир)

        к.путања_интервали = providers.Callable(lambda дир: дир.joinpath('интервали.tsv'), к.дир)
        к.путања_карте = providers.Callable(lambda дир: дир.joinpath('карте.tsv'), к.дир)
        к.путања_линкови = providers.Callable(lambda дир: дир.joinpath('линкови.tsv'), к.дир)
        к.путања_запис = providers.Callable(lambda дир: дир.joinpath('запис.tsv'), к.дир)

        к.т_интервала = providers.Callable(Табела, путања=к.путања_интервали, Тип=Интервали)
        к.т_карти = providers.Factory(Табела, путања=к.путања_карте, Тип=Карта)
        к.т_линкова = providers.Factory(Табела, путања=к.путања_линкови, Тип=Линк)
        к.т_записа = providers.Factory(Табела, путања=к.путања_запис, Тип=Запис)

        к.п_интервала = providers.Factory(ПогледИнтервала, табела=к.т_интервала)
        к.п_карти = providers.Factory(ПогледКарти, табела=к.т_карти)
        к.п_линкова = providers.Factory(ПогледЛинкова, табела=к.т_линкова)
        к.п_записа = providers.Factory(ПогледЗаписа, табела=к.т_записа)

        к.шпил = providers.Factory(
            Шпил,
            питање_ui=к.отац.питање_ui,
            одговор_ui=к.отац.одговор_ui,
            дир=к.дир,
            п_интервала=к.п_интервала,
            п_карти=к.п_карти,
            п_линкова=к.п_линкова,
            п_записа=к.п_записа)


class Контејнер(containers.DynamicContainer):
    def листа_дирова(к, каталог):
        return [фајл for фајл in каталог.iterdir() if фајл.is_dir() and not фајл.name.startswith('__')]

    def листа_шпилова(к):
        return [ШпилКонтејнер(отац=к, дир=дир).шпил() for дир in к.дирови()]

    def __init__(к):
        super().__init__()
        к.каталог = providers.Object(ПУТАЊА_КАТАЛОГА)
        к.дирови = providers.Callable(к.листа_дирова, каталог=к.каталог)
        к.шпилови = providers.Callable(к.листа_шпилова)
        к.терминал = providers.Singleton(Терминал)
        к.регистар = providers.Factory(Регистар)
        к.главна_ui = providers.Factory(ГлавнаUI, терминал=к.терминал, регистар=к.регистар)
        к.питање_ui = providers.Factory(ПитањеUI, терминал=к.терминал, регистар_питање=к.регистар)
        к.одговор_ui = providers.Factory(ОдговорUI, терминал=к.терминал, регистар_одговор=к.регистар)
        к.главна = providers.Factory(Главна, ui=к.главна_ui, шпилови=к.шпилови)


def главна():
    г = Контејнер().главна()
    г.припреми()
    г()


if __name__ == '__main__':
    главна()

