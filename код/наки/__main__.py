from наки import одабир
from наки.терминал import Терминал
from наки.конфигурација import ПУТАЊА_КАТАЛОГА
from наки.вежбање import Вежбање


def учитај_вежбања(каталог):
    шпилови = [шпил for шпил in каталог.iterdir() if шпил.is_dir() and not шпил.name.startswith('__')]
    return [Вежбање(шпил) for шпил in шпилови]


class Главна():

    def __init__(бре, терминал, вежбања):
        бре.терминал = терминал
        бре.вежбања = вежбања

    def одабери_шпил(бре, команде):
        приказ = [f"[{len(в)}] {в.име_шпила()}" for в in бре.вежбања]
        порука = 'бројем одабери шпил, "и" да избациш промашене, "п" да преполовиш, "к" за крај'
        индекс = одабир.један(бре.терминал, приказ, порука, команде)
        return индекс

    def __call__(бре):
        избаци_промашене = ['i', 'и']
        преполови = ['p', 'п']
        крај = ['k', 'к']
        команде = []
        команде.extend(избаци_промашене)
        команде.extend(преполови)
        команде.extend(крај)
        while True:
            индекс = бре.одабери_шпил(команде)
            if индекс in избаци_промашене:
                for в in бре.вежбања:
                    в.избаци_промашене()
            elif индекс in преполови:
                for в in бре.вежбања:
                    в.преполови()
            elif индекс in крај:
                return бре.вежбања
            else:
                бре.вежбања[индекс - 1](бре.терминал)


def главна():
    вежбања = учитај_вежбања(ПУТАЊА_КАТАЛОГА)
    вежбања.sort(key=lambda в: len(в))
    Главна(Терминал(), вежбања)()


if __name__ == '__main__':
    главна()
