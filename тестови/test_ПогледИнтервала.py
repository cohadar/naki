import pytest
import datetime
from pathlib import Path
from наки.интервали import ПогледИнтервала, Интервали
from тест.tsv import ТестТабела

И = Интервали("ДАМИР",  datetime.date(2020, 5, 17), [1, 7, 15, 38, 94, 234, 586, 1465, 3662])


def СИРОВИ():
    сирови = [['ВРСТА_КАРТЕ', 'ДАТУМ', 'ИНТЕРВАЛИ']]
    сирови.append(["ДАМИР", "2020-04-16", "1, 6, 15, 38, 94, 234, 586, 1465, 3662"])
    сирови.append(["ДАМИР", "2020-05-17", "1, 7, 15, 38, 94, 234, 586, 1465, 3662"])
    сирови.append(["ДАМИР", "2020-04-14", "1, 6, 15, 38, 94, 234, 586, 1465, 3662"])
    сирови.append(["BBB", "2020-04-17", "1, 6, 15, 38, 94, 234, 586, 1465, 3662"])
    сирови.append(["CCC", "2020-04-17", "1, 9, 15, 38, 94, 234, 586, 1465, 3662"])
    return сирови


def ПИВ():
    ти = ТестТабела(Path('интервали.tsv'), Интервали, СИРОВИ())
    return ПогледИнтервала(ти), ти


def test_парсирање():
    пи, ти = ПИВ()
    ит = iter(ти)
    next(ит)
    и = next(ит)
    assert и == И


def test_има_врсту_карте():
    пи, ти = ПИВ()
    assert пи.има_врсту_карте("ДАМИР")
    assert пи.има_врсту_карте("BBB")
    assert пи.има_врсту_карте("CCC")
    assert not пи.има_врсту_карте("ZZZ")


def test_консолидуј():
    пи, ти = ПИВ()
    assert len(пи) == 5
    с = set()
    с.add('ДАМИР')
    пи.консолидуј(с)
    assert len(пи) == 5
    с.add('МЕХ')
    пи.консолидуј(с)
    assert len(пи) == 6


def test_период_интервала():
    пи, ти = ПИВ()
    assert пи.период_интервала('ДАМИР', 1) == 7


def test_период_интервала_нема():
    пи, ти = ПИВ()
    with pytest.raises(KeyError):
        пи.период_интервала('НЕПОЗНАТ', 1)

