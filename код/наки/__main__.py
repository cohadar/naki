from наки.конфигурација import ПУТАЊА_КАТАЛОГА
from наки.вежбање import Вежбање
from наки.шпил import Шпил
from наки.главна import Главна
from наки.терминал import Терминал
from наки.ui import UI
from наки.интервали import ПогледИнтервала, Интервали
from наки.запис import ПогледЗаписа, Запис
from наки.линкови import ПогледЛинкова, Линк
from наки.карте import ПогледКарти, Карта
from наки.tsv import Табела
import dependency_injector.containers as containers
import dependency_injector.providers as providers


class ШпилКонтејнер(containers.DynamicContainer):
    def __init__(к, дир):
        super().__init__()
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
            дир=к.дир,
            п_интервала=к.п_интервала,
            п_карти=к.п_карти,
            п_линкова=к.п_линкова,
            п_записа=к.п_записа)


class Контејнер(containers.DynamicContainer):
    def листа_дирова(к, каталог):
        return [фајл for фајл in каталог.iterdir() if фајл.is_dir() and not фајл.name.startswith('__')]

    def листа_шпил_контејнера(к):
        return [ШпилКонтејнер(дир=дир) for дир in к.дирови()]

    def листа_вежбања(к):
        return [Вежбање(ui=к.ui(), путања_каталога=к.каталог(), шпил=шк.шпил()) for шк in к.шпил_контејнери()]

    def __init__(к):
        super().__init__()
        к.каталог = providers.Object(ПУТАЊА_КАТАЛОГА)
        к.дирови = providers.Callable(к.листа_дирова, каталог=к.каталог)
        к.шпил_контејнери = providers.Callable(к.листа_шпил_контејнера)
        к.терминал = providers.Factory(Терминал)
        к.ui = providers.Singleton(UI, терминал=к.терминал)
        к.вежбања = providers.Callable(к.листа_вежбања)
        к.главна = providers.Factory(Главна, ui=к.ui, вежбања=к.вежбања)


def главна():
    Контејнер().главна()()


if __name__ == '__main__':
    главна()

