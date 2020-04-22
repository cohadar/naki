from pathlib import Path
from наки.карте import ПогледКарти, Карта
from тест.tsv import ТестТабела
from тест.насумично import карте


def СИРОВИ():
    сирови = [['ИД', 'ВРСТА_КАРТЕ', 'ПИТАЊЕ', 'ОДГОВОР', 'ИЗВОР', 'ЛИНИЈА']]
    сирови.extend(карте(100))
    return сирови


def ПК():
    тт = ТестТабела(Path('карте.tsv'), Карта, СИРОВИ())
    return ПогледКарти(тт), тт


def test_init():
    пк, тт = ПК()
    assert len(тт) == 100
    assert len(пк) == 100


def test_филтрирај():
    пк, тт = ПК()
    пк.филтрирај(lambda и, ид, вк: (и % 2) != 0)
    assert len(пк) == 50

