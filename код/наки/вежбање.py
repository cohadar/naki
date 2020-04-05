import os
import sys
import subprocess
from наки.команда import КОМАНДА_ПРЕКИД, КОМАНДА_ОТВОРИ_УРЛ, КОМАНДА_ЕДИТУЈ
from наки.команда import КОМАНДА_ФЕЈЛ, КОМАНДА_ПЛУС1, КОМАНДА_ПЛУС2
from наки.карте import Карта


def отвори_урл(урл):
    if sys.platform == 'win32':
        os.startfile(урл)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', урл])
    else:
        subprocess.Popen(['xdg-open', урл])


def измени(путања_каталога, лепа_путања, линија):
    права_путања = путања_каталога.joinpath(лепа_путања)
    subprocess.run(['vim', '+' + линија, '+normal_WW', str(права_путања)])


def питање_и_одговор(терминал, путања_каталога, карта, број_преосталих_карата, урл):
    терминал.обриши()
    with терминал.главни():
        терминал.принт_наслов(карта[Карта.ВРСТА_КАРТЕ.value])
        терминал.принт_мд(карта[Карта.ПИТАЊЕ.value])
        терминал.принт_сепаратор('-')
        with терминал.статус():
            терминал.принт_сепаратор('=', број_преосталих_карата)
            терминал.принт('притисни било који тастер')
        while True:
            к = терминал.инпут_код()
            if к in КОМАНДА_ПРЕКИД:
                return (True, None)
            if к in КОМАНДА_ОТВОРИ_УРЛ:
                if урл:
                    отвори_урл(урл)
                else:
                    терминал.звук_грешке()
                continue
            if к in КОМАНДА_ЕДИТУЈ:
                измени(путања_каталога, карта[Карта.ИЗВОР.value], карта[Карта.ЛИНИЈА.value])
                continue
            break
        терминал.принт_мд(карта[Карта.ОДГОВОР.value])
        with терминал.статус():
            терминал.принт_сепаратор('=', број_преосталих_карата)
            терминал.принт('оцени одговор (f: 0)(space: +1)(enter: +2)')
        ДОЗВОЉЕНЕ = [КОМАНДА_ПРЕКИД, КОМАНДА_ОТВОРИ_УРЛ, КОМАНДА_ЕДИТУЈ, КОМАНДА_ФЕЈЛ, КОМАНДА_ПЛУС1, КОМАНДА_ПЛУС2]

        def екстра(и):
            for к in ДОЗВОЉЕНЕ:
                if и in к:
                    return к
            return None

        while True:
            к = терминал.инпут_код(екстра)
            if к in КОМАНДА_ПРЕКИД:
                return (True, None)
            elif к in КОМАНДА_ОТВОРИ_УРЛ:
                if урл:
                    отвори_урл(урл)
                else:
                    терминал.звук_грешке()
                continue
            elif к in КОМАНДА_ЕДИТУЈ:
                измени(карта[Карта.ИЗВОР.value], карта[Карта.ЛИНИЈА.value])
                continue
            elif к in КОМАНДА_ФЕЈЛ:
                return (False, 0)
            elif к in КОМАНДА_ПЛУС1:
                return (False, 1)
            elif к in КОМАНДА_ПЛУС2:
                return (False, 2)
            else:
                raise Exception(f'непозната команда: {к}')


class Вежбање():
    def __init__(бре, путања_каталога, шпил):
        бре.шпил = шпил
        бре.путања_каталога = путања_каталога

    def име_шпила(бре):
        return бре.шпил.име()

    def __len__(бре):
        return len(бре.шпил)

    def __call__(бре, терминал):
        бре.шпил.рандомизуј()
        неодрађене = set(карта[Карта.ИД] for карта in бре.шпил)
        промашене = set()
        for карта in бре.шпил:
            ид = карта[Карта.ИД]
            урл = бре.шпил.урл(ид)
            број_карата = f"{len(неодрађене)}+{len(промашене)}"
            прекид, оцена = питање_и_одговор(терминал, бре.путања_каталога, карта, број_карата, урл)
            if прекид:
                break
            бре.шпил.оцена(ид, оцена)
            неодрађене.discard(ид)
            if оцена > 0:
                промашене.discard(ид)
            else:
                промашене.add(ид)
        бре.шпил.clear()

    def __eq__(бре, други):
        if not isinstance(други, Вежбање):
            return False
        return бре.шпил == други.шпил

    def __repr__(бре):
        return f"{бре.шпил}"

    def преполови(бре):
        бре.шпил.преполови()

    def избаци_промашене(бре):
        бре.шпил.избаци_промашене()
