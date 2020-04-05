import os
import subprocess
import sys
import time
import random
from datetime import date, timedelta
from collections import Counter, defaultdict
from enum import IntEnum, unique
from наки import tsv
from random import shuffle
from pathlib import Path
from наки.конфигурација import ПУТАЊА_КАТАЛОГА


@unique
class Карта(IntEnum):
    ИД = 0
    ВРСТА_КАРТЕ = 1
    ПИТАЊЕ = 2
    ОДГОВОР = 3
    ИЗВОР = 4
    ЛИНИЈА = 5


@unique
class Запис(IntEnum):
    КАРТА_ИД = 0
    ДАТУМ_ПРЕГЛЕДА = 1
    ВРЕМЕ_ПРЕГЛЕДА = 2
    РЕЗУЛТАТ_ПРЕГЛЕДА = 3
    НОВИ_ИНТЕРВАЛ = 4


@unique
class Линк(IntEnum):
    ИД = 0
    УРЛ = 1


@unique
class Интервали(IntEnum):
    ДАТУМ = 0
    И1 = 1
    И2 = 2
    И3 = 3
    И4 = 4
    И5 = 5
    И6 = 6
    И7 = 7
    И8 = 8
    И9 = 9


МАКС_ИНТЕРВАЛ = len(Интервали)


def направи_карте(извор_фајл, извор, врста_карте, ф_питање, ф_одговор, индекс):
    """ постарај се да индекс буде јединствен при сваком позиву """
    assert 0 <= индекс and индекс < 16
    карте = []
    for линија, џ in enumerate(извор, 2):
        ид = џ[0]  # претпоставка је да је нулто поље ИД
        assert ид[-1] == '0', 'извор ид мора да се завршава са нулом: ' + ид
        ид = ид[:-1] + hex(индекс)[-1]
        карте.append([ид, врста_карте, ф_питање(џ), ф_одговор(џ), извор_фајл, линија])
    return карте


def отвори_урл(урл):
    if sys.platform == 'win32':
        os.startfile(урл)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', урл])
    else:
        subprocess.Popen(['xdg-open', урл])


def измени(лепа_путања, линија):
    права_путања = ПУТАЊА_КАТАЛОГА.joinpath(лепа_путања)
    subprocess.run(['vim', '+' + линија, '+normal_WW', str(права_путања)])


def питање_и_одговор(терминал, карта, број_преосталих_карата, урл):
    терминал.обриши()
    with терминал.главни():
        терминал.принт_наслов(карта[Карта.ВРСТА_КАРТЕ.value])
        терминал.принт_мд(карта[Карта.ПИТАЊЕ.value])
        терминал.принт_сепаратор('-')
        with терминал.статус():
            терминал.принт_сепаратор('=', број_преосталих_карата)
            терминал.принт('притисни било који тастер')
        while True:
            к = терминал.учитај_кључ()
            if к == терминал.CYR_O:
                к = 'o'
            if к == терминал.CYR_F:
                к = 'f'
            if к == терминал.CYR_E:
                к = 'e'
            if терминал.јели_прекид_кључ(к):
                return (True, None)
            if к == 'o':
                if урл:
                    отвори_урл(урл)
                else:
                    терминал.звук_грешке()
                continue
            if к == 'e':
                измени(карта[Карта.ИЗВОР.value], карта[Карта.ЛИНИЈА.value])
                continue
            break
        терминал.принт_мд(карта[Карта.ОДГОВОР.value])
        with терминал.статус():
            терминал.принт_сепаратор('=', број_преосталих_карата)
            терминал.принт('оцени одговор (f: 0)(space: +1)(enter: +2)')
        КЉУЧЕВИ = ['f', 'o', 'e', терминал.СПЕЈС, терминал.ЕНТЕР, терминал.CYR_F, терминал.CYR_O, терминал.CYR_E]
        оцена = -1
        while True:
            к = терминал.учитај_кључ(КЉУЧЕВИ)
            if к == терминал.CYR_O:
                к = 'o'
            if к == терминал.CYR_F:
                к = 'f'
            if к == терминал.CYR_E:
                к = 'e'
            if к == 'o':
                if урл:
                    отвори_урл(урл)
                else:
                    терминал.звук_грешке()
                continue
            if к == 'e':
                измени(карта[Карта.ИЗВОР.value], карта[Карта.ЛИНИЈА.value])
                continue
            if к in КЉУЧЕВИ:
                if к == 'f':
                    оцена = 0
                elif к == терминал.СПЕЈС:
                    оцена = 1
                elif к == терминал.ЕНТЕР:
                    оцена = 2
                else:
                    raise Exception(f'немогућ к: {к}')
                return (False, оцена)
            if терминал.јели_прекид_кључ(к):
                return (True, None)
            raise Exception("не би требало да се деси")


def учитај_запис(путања):
    нови_интервал = Counter()
    датум_прегледа = {}
    if путања.exists():
        запис = tsv.учитај_фајл(путања, Запис)
        for з in запис:
            if int(з[Запис.РЕЗУЛТАТ_ПРЕГЛЕДА]) > 0:
                нови_интервал[з[Запис.КАРТА_ИД]] = int(з[Запис.НОВИ_ИНТЕРВАЛ])
                датум_прегледа[з[Запис.КАРТА_ИД]] = date.fromisoformat(з[Запис.ДАТУМ_ПРЕГЛЕДА])
    return (нови_интервал, датум_прегледа)


def може_данас(ид, интервали, нови_интервал, датум_прегледа):
    данас = date.today()
    давно = date.fromisoformat('1970-01-01')
    дп = датум_прегледа.get(ид, давно)
    ни = timedelta(days=интервали[нови_интервал[ид]-1])
    return данас > дп + ни


def рандомизуј(карте):
    по_врсти = defaultdict(list)
    for карта in карте:
        врста = карта[Карта.ВРСТА_КАРТЕ]
        по_врсти[врста].append(карта)
    рет = []
    for в in по_врсти.values():
        shuffle(в)
        рет.extend(в)
    return рет


def провера_јединствености(карте):
    нађено = False
    дупло = set()
    for карта in карте:
        питање = f"{карта[Карта.ВРСТА_КАРТЕ]}: {карта[Карта.ПИТАЊЕ]}"
        if питање in дупло:
            print(f"ДУПЛИКАТ: {питање}", file=sys.stderr)
            нађено = True
        дупло.add(питање)
    if нађено:
        sys.exit(1)


def активне_карте(карте, интервали, нови_интервал, датум_прегледа):
    провера_јединствености(карте)
    активне = set()
    for карта in карте:
        ид = карта[Карта.ИД]
        if може_данас(ид, интервали, нови_интервал, датум_прегледа):
            активне.add(ид)
    return активне


def учитај(путања):
    интервали_путања = Path(путања).joinpath('интервали.tsv')
    запис_путања = Path(путања).joinpath('запис.tsv')
    карте_путања = Path(путања).joinpath('карте.tsv')
    интервали = tsv.учитај_фајл(интервали_путања, Интервали)
    интервали = интервали[-1][1:]
    интервали = [int(и) for и in интервали]
    нови_интервал, датум_прегледа = учитај_запис(запис_путања)
    карте = tsv.учитај_фајл(карте_путања, Карта)
    активне = активне_карте(карте, интервали, нови_интервал, датум_прегледа)
    return интервали, карте, активне, нови_интервал, запис_путања


def извор_ид(карта_ид):
    return карта_ид[:-1] + '0'


def вежбање(терминал, путања, макс_активних):
    интервали, карте, активне, нови_интервал, запис_путања = учитај(путања)
    линк_мапа = {}
    линкови_путања = Path(путања).joinpath('линкови.tsv')
    if линкови_путања.exists():
        линкови = tsv.учитај_фајл(линкови_путања, Линк)
        for л in линкови:
            линк_мапа[л[Линк.ИД]] = л[Линк.УРЛ]
    # индекс = одабир.један(терминал, ['да', 'не'], 'рандомизуј унутар врсте карте?')
    # if индекс == 1:
    #     карте = рандомизуј(карте)
    карте = рандомизуј(карте)
    промашене = set()
    активне = set(random.sample(активне, макс_активних))
    for карта in карте:
        ид = карта[Карта.ИД]
        if ид in активне:
            урл = линк_мапа.get(извор_ид(карта[Карта.ИД]))
            број_карата = f"{len(активне) - len(промашене)}+{len(промашене)}"
            прекид, оцена = питање_и_одговор(терминал, карта, број_карата, урл)
            if прекид:
                активне.clear()
                break
            нови_интервал[ид] = min(нови_интервал[ид] + оцена, МАКС_ИНТЕРВАЛ)
            ред = [
                ид,
                time.strftime('%Y-%m-%d'),
                time.strftime('%H:%M:%S%z'),
                оцена,
                нови_интервал[ид],
            ]
            tsv.додај_на_фајл(запис_путања, Запис, [ред])
            if оцена > 0:
                активне.remove(ид)
                промашене.discard(ид)
            else:
                промашене.add(ид)


def шпил(терминал, путања, макс_активних):
    with терминал.сакривен_курсор():
        вежбање(терминал, путања, макс_активних)


def број_активних(путања):
    интервали, карте, активне, нови_интервал, запис_путања = учитај(путања)
    return len(активне)


class Вежбање():

    @staticmethod
    def учитај_интервале(путања):
        интервали = tsv.учитај_фајл(путања, Интервали)
        интервали = интервали[-1][1:]
        return [int(и) for и in интервали]

    @staticmethod
    def учитај_запис(путања):
        нови_интервал = Counter()
        датум_прегледа = {}
        последња_оцена = {}
        if путања.exists():
            запис = tsv.учитај_фајл(путања, Запис)
            for з in запис:
                оцена = int(з[Запис.РЕЗУЛТАТ_ПРЕГЛЕДА])
                последња_оцена[з[Запис.КАРТА_ИД]] = оцена
                if оцена > 0:
                    нови_интервал[з[Запис.КАРТА_ИД]] = int(з[Запис.НОВИ_ИНТЕРВАЛ])
                    датум_прегледа[з[Запис.КАРТА_ИД]] = date.fromisoformat(з[Запис.ДАТУМ_ПРЕГЛЕДА])
        return (нови_интервал, датум_прегледа, последња_оцена)

    @staticmethod
    def учитај_линкове(путања):
        линк_мапа = {}
        if путања.exists():
            линкови = tsv.учитај_фајл(путања, Линк)
            for л in линкови:
                линк_мапа[л[Линк.ИД]] = л[Линк.УРЛ]
        return линк_мапа

    def може_данас(бре, ид):
        данас = date.today()
        давно = date.fromisoformat('1970-01-01')
        дп = бре.датум_прегледа.get(ид, давно)
        ни = timedelta(days=бре.интервали[бре.нови_интервал[ид]-1])
        return данас > дп + ни

    @staticmethod
    def провера_јединствености(карте):
        нађено = False
        дупло = set()
        for карта in карте:
            питање = f"{карта[Карта.ВРСТА_КАРТЕ]}: {карта[Карта.ПИТАЊЕ]}"
            if питање in дупло:
                print(f"ДУПЛИКАТ: {питање}", file=sys.stderr)
                нађено = True
            дупло.add(питање)
        if нађено:
            sys.exit(1)

    def учитај_активне_карте(бре, путања):
        карте = tsv.учитај_фајл(путања, Карта)
        бре.провера_јединствености(карте)
        return [карта for карта in карте if бре.може_данас(карта[Карта.ИД])]

    def __init__(бре, шпил):
        бре.шпил = шпил
        бре.интервали = бре.учитај_интервале(шпил.joinpath('интервали.tsv'))
        бре.запис_путања = шпил.joinpath('запис.tsv')
        бре.нови_интервал, бре.датум_прегледа, бре.последња_оцена = бре.учитај_запис(бре.запис_путања)
        бре.линк_мапа = бре.учитај_линкове(шпил.joinpath('линкови.tsv'))
        бре.активне = бре.учитај_активне_карте(шпил.joinpath('карте.tsv'))

    def име_шпила(бре):
        return бре.шпил.наме

    def __len__(бре):
        return len(бре.активне)

    def рандомизуј(бре):
        по_врсти = defaultdict(list)
        for карта in бре.активне:
            врста = карта[Карта.ВРСТА_КАРТЕ]
            по_врсти[врста].append(карта)
        темп = []
        for в in по_врсти.values():
            shuffle(в)
            темп.extend(в)
        бре.активне = темп

    @staticmethod
    def извор_ид(карта_ид):
        return карта_ид[:-1] + '0'

    def __call__(бре, терминал):
        бре.рандомизуј()
        неодрађене = set(карта[Карта.ИД] for карта in бре.активне)
        промашене = set()
        for карта in бре.активне:
            ид = карта[Карта.ИД]
            урл = бре.линк_мапа.get(бре.извор_ид(карта[Карта.ИД]))
            број_карата = f"{len(неодрађене)}+{len(промашене)}"
            прекид, оцена = питање_и_одговор(терминал, карта, број_карата, урл)
            if прекид:
                break
            бре.нови_интервал[ид] = min(бре.нови_интервал[ид] + оцена, МАКС_ИНТЕРВАЛ)
            ред = [
                ид,
                time.strftime('%Y-%m-%d'),
                time.strftime('%H:%M:%S%z'),
                оцена,
                бре.нови_интервал[ид],
            ]
            tsv.додај_на_фајл(бре.запис_путања, Запис, [ред])
            неодрађене.discard(ид)
            if оцена > 0:
                промашене.discard(ид)
            else:
                промашене.add(ид)
        бре.активне.clear()

    def преполови(бре):
        бре.активне = бре.активне[::2]

    def избаци_промашене(бре):
        бре.активне = [к for к in бре.активне if бре.последња_оцена.get(к[Карта.ИД], 0) > 0]
