import pytest
import datetime
from pathlib import Path
from наки.карте import ПогледКарти, Карта
from тест.tsv import ТестТабела


def СИРОВИ():
    сирови = [['ИД', 'ВРСТА_КАРТЕ', 'ПИТАЊЕ', 'ОДГОВОР', 'ИЗВОР', 'ЛИНИЈА']]
    сирови.append(["eb31196dc7fb426b845193a814048120", "vk1", "p1", "o1", "put1", "1"])
    return сирови


def ПК():
    тт = ТестТабела(Path('карте.tsv'), Карта, СИРОВИ())
    тт.учитај()
    return ПогледКарти(тт), тт


def test_init():
    пк, тт = ПК()

