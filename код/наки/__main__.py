import os
import sys
import readchar
import subprocess
from blessings import Terminal
from наки.терминал import Терминал
from наки.конфигурација import ПУТАЊА_КАТАЛОГА
from наки.вежбање import Вежбање
from наки.команда import КОМАНДА_ПРЕКИД, КОМАНДА_ИЗБАЦИ_ПРОМАШЕНЕ, КОМАНДА_ПРЕПОЛОВИ
from наки.карте import Шпил, ШпилДиск


def учитај_вежбања(каталог):
    дирови = [фајл for фајл in каталог.iterdir() if фајл.is_dir() and not фајл.name.startswith('__')]
    return [Вежбање(каталог, Шпил(ШпилДиск(дир))) for дир in дирови]


class Главна():

    def __init__(бре, терминал, вежбања):
        бре.терминал = терминал
        бре.вежбања = вежбања

    def одабери_шпил(бре, екстра):
        приказ = [f"[{len(в)}] {в.име_шпила()}" for в in бре.вежбања]
        порука = 'бројем одабери шпил, "и" да избациш промашене, "п" да преполовиш, "к" за крај'
        индекс = бре.терминал.одабери_један(приказ, порука, екстра)
        return индекс

    def __call__(бре):
        екстра_команде = [КОМАНДА_ПРЕКИД, КОМАНДА_ИЗБАЦИ_ПРОМАШЕНЕ, КОМАНДА_ПРЕПОЛОВИ]

        def екстра(и):
            for к in екстра_команде:
                if и in к:
                    return к
            return None

        while True:
            к = бре.одабери_шпил(екстра)
            if к in КОМАНДА_ИЗБАЦИ_ПРОМАШЕНЕ:
                for в in бре.вежбања:
                    в.избаци_промашене()
            elif к in КОМАНДА_ПРЕПОЛОВИ:
                for в in бре.вежбања:
                    в.преполови()
            elif к in КОМАНДА_ПРЕКИД:
                return [в.сиже() for в in бре.вежбања]
            else:
                бре.вежбања[к - 1](бре.терминал)


def измени(путања, линија):
    subprocess.run(['vim', '+' + линија, '+normal_WW', str(путања)])


def отвори_урл(урл):
    if sys.platform == 'win32':
        os.startfile(урл)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', урл])
    else:
        subprocess.Popen(['xdg-open', урл])


def звук_грешке():
    print('\a', end='', flush=True)


def главна():
    вежбања = учитај_вежбања(ПУТАЊА_КАТАЛОГА)
    вежбања.sort(key=lambda в: len(в))
    terminal = Terminal()
    # залепи сирове метода на терминал објекат, лакше него завити у нову класу
    terminal.readkey = readchar.readkey
    terminal.input = input
    terminal.print = print
    terminal.измени = измени
    terminal.звук_грешке = звук_грешке
    terminal.отвори_урл = отвори_урл
    # ајмо
    Главна(Терминал(terminal), вежбања)()


if __name__ == '__main__':
    главна()
