import time
import uuid
import random
from pathlib import Path
from hashlib import sha256
from каталог.__main__ import направи_карте
from наки.__main__ import Контејнер
import dependency_injector.providers as providers
from тест.tsv import Табела
from тест.терминал import ТестТерминал
from наки.интервали import Интервали
from наки.запис import Запис
from наки.линкови import Линк
from наки.карте import Карта


def фајл_хеш(path1):
    with open(path1, 'r') as ф:
        садржај = ф.read()
        м = sha256()
        м.update(bytes(садржај, 'utf-8'))
        return м.hexdigest()


class ТестКонтејнер(Контејнер):
    def __init__(к, команде, дужине):
        super().__init__()
        к.команде = providers.Object(команде)
        к.дужине = providers.Object(дужине)
        к.каталог = providers.Object(Path('лажни-каталог'))
        к.терминал.override(providers.Factory(ТестТерминал, команде=к.команде))

    def листа_дирова(к, каталог):
        return [Path('дир').joinpath(str(и)) for и in range(len(к.дужине()))]

    def листа_вежбања(к):
        рез = []
        for дир, лен in zip(к.дирови(), к.дужине()):
            к.дир.override(providers.Object(дир))
            к.шпил_лоадер(дир, лен)
            к.т_интервала.override(
                providers.Factory(Табела, путања=к.путања_интервали, Тип=Интервали, на_диску=к.д_интервали))
            к.т_карти.override(
                providers.Factory(Табела, путања=к.путања_карте, Тип=Карта, на_диску=к.д_карте))
            к.т_линкова.override(
                providers.Factory(Табела, путања=к.путања_линкови, Тип=Линк, на_диску=к.д_линкови))
            к.т_записа.override(
                providers.Factory(Табела, путања=к.путања_запис, Тип=Запис, на_диску=к.д_запис))
            рез.append(к.вежбање())
        return рез

    def шпил_лоадер(к, дир, лен):
        дир = Path(дир)
        карте = []
        линкови = []
        for извор_фајл in ['aaa.tsv', 'bbb.tsv', 'ccc.tsv']:
            лепа_путања = дир.joinpath('извор', извор_фајл)
            извор = извор_учитај(извор_фајл)
            ка, ли = извор_одради(лепа_путања, извор)
            карте.extend(ка)
            линкови.extend(ли)
        карте = карте[:лен]
        скуп_врста_карте = set()
        ВРСТА_КАРТЕ = 1  # индекс поља
        for карта in карте:
            скуп_врста_карте.add(карта[ВРСТА_КАРТЕ])
        интервали = []
        for врста_карте in скуп_врста_карте:
            интервали.append([врста_карте, "2019-12-07", "1, 6, 15, 38, 94, 234, 586, 1465, 3662"])
        линкови = линкови[:лен]
        запис = []
        for и, карта in enumerate(карте):
            if и % 4 == 0:
                запис.append([карта[0], "2020-03-28", "3:34:53+0100", "0", "1"])
            # TODO dodaj pregledane danas, isto kao cetvrtinu

        к.д_интервали = [['ВРСТА_КАРТЕ', 'ДАТУМ', 'ИНТЕРВАЛИ']]
        к.д_интервали.extend(интервали)

        к.д_карте = [['ИД', 'ВРСТА_КАРТЕ', 'ПИТАЊЕ', 'ОДГОВОР', 'ИЗВОР', 'ЛИНИЈА']]
        к.д_карте.extend(карте)

        к.д_линкови = [['ИД', 'УРЛ']]
        к.д_линкови.extend(линкови)

        к.д_запис = [['КАРТА_ИД', 'ДАТУМ_ПРЕГЛЕДА', 'ВРЕМЕ_ПРЕГЛЕДА', 'РЕЗУЛТАТ_ПРЕГЛЕДА', 'НОВИ_ИНТЕРВАЛ']]
        к.д_запис.extend(запис)



def направи_линк(извор):
    ид = извор[0]
    питање = 'ли' + str(random.random())[2:]
    return [ид, f"https://www.google.de/search?tbm=isch&q={питање}"]


def извор_одради(лепа_путања, извор):
    карте = []
    индекс = iter(range(16))

    # 0, 1
    def питање(џ):
        return 'пи' + str(random.random())[2:]

    def одговор(џ):
        return 'од' + str(random.random())[2:]

    for и in range(1, 12):
        карте.extend(направи_карте(лепа_путања, извор, f"ТИП{и}", питање, одговор, next(индекс)))
    линкови = [направи_линк(и) for и in извор]
    return карте, линкови


def _рандом_датум():
    пет_година = 60*60*24*365*5
    данас = time.mktime(time.localtime())
    датум = time.localtime(данас - random.randint(0, пет_година))
    return time.strftime("%Y-%m-%d", датум)


def извор_учитај(путања):
    рез = []
    for _ in range(10):
        рез.append([
            uuid.uuid4().hex[:-1] + '0',
            _рандом_датум(),
            'ле' + str(random.random())[2:],
            'де' + str(random.random())[2:],
        ])
    return рез


