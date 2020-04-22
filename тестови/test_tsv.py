import csv
import pytest
from наки import tsv
from наки.tsv import Табела
from тест.tsv import ТестТабела
from pathlib import Path
from shutil import copy
from тест.тест import фајл_хеш
from collections import namedtuple


Елемент = namedtuple('Елемент', ['ид', 'датум', 'инфинитив', 'презент', 'претерит', 'перфект', 'превод'])
Елемент = tsv.namedtuple(Елемент)


ЕЛЕМЕНТИ = [
    Елемент('4157813edfb24ffc952f1bd9ccf1d9b6', '2019-12-07',
            'dürfen', 'darf', 'durfte', 'hat gedurft', 'smeti'),
    Елемент('f8924411091446248d30895d161966fb', '2019-12-07',
            'empfehlen', 'empfiehlt', 'empfahl', 'hat empfohlen', 'preporučiti'),
]


def са_диска(табела):
    на_диску = []
    assert isinstance(табела._путања, Path), табела._путања
    with табела._путања.open('r', newline='') as ф:
        tsv = csv.reader(ф, delimiter='\t')
        for ред in tsv:
            на_диску.append(ред)
    return ТестТабела(табела._путања, табела._Тип, на_диску)


def test_учитај_фајл():
    т = Табела(Path('тест-фајлови/tsv/ok10.tsv'), Елемент)
    тт = са_диска(т)
    т.учитај()
    assert len(т) == 10
    тт.учитај()
    assert len(тт) == 10


def test_учитај_фајл_идемпотентна():
    т = tsv.Табела(Path('тест-фајлови/tsv/ok10.tsv'), Елемент)
    тт = са_диска(т)
    т.учитај()
    т.учитај()
    assert len(т) == 10
    тт.учитај()
    тт.учитај()
    assert len(тт) == 10


def test_учитај_фајл_рет():
    т = tsv.Табела(Path('тест-фајлови/tsv/ok10.tsv'), Елемент)
    тт = са_диска(т)
    assert id(т.учитај()) == id(т)
    assert id(тт.учитај()) == id(тт)


def test_учитај_фајл_КолонеПогрешнаВеличина():
    т = tsv.Табела(Path('тест-фајлови/tsv/tabfali.tsv'), Елемент)
    тт = са_диска(т)
    with pytest.raises(tsv.ПарсирањеГрешка):
        т.учитај()
    with pytest.raises(tsv.ПарсирањеГрешка):
        тт.учитај()


def test_учитај_фајл_КолонеИменаСеНеПоклапају():
    т = tsv.Табела(Path('тест-фајлови/tsv/drugitip.tsv'), Елемент)
    тт = са_диска(т)
    with pytest.raises(tsv.ЗаглављеГрешка):
        т.учитај()
    with pytest.raises(tsv.ЗаглављеГрешка):
        тт.учитај()


def test_додај_на_фајл_постоји(tmpdir):
    copy('тест-фајлови/tsv/ok08.tsv', tmpdir)
    путања = Path(tmpdir).joinpath('ok08.tsv')
    т = tsv.Табела(путања, Елемент)
    тт = са_диска(т)
    т.додај(ЕЛЕМЕНТИ)
    assert фајл_хеш('тест-фајлови/tsv/ok10.tsv') == фајл_хеш(путања)
    тт.додај(ЕЛЕМЕНТИ)
    assert тт._елементи == т._елементи


def test_додај_на_фајл_непостоји(tmpdir):
    путања = Path(tmpdir).joinpath('ok_ново.tsv')
    т = tsv.Табела(путања, Елемент)
    т.додај(ЕЛЕМЕНТИ)
    assert фајл_хеш('тест-фајлови/tsv/ok02.tsv') == фајл_хеш(путања)
    тт = ТестТабела(т._путања, т._Тип, [])
    тт.додај(ЕЛЕМЕНТИ)
    assert тт._елементи == т._елементи


def test_додај_на_фајл_КолонеИменаСеНеПоклапају(tmpdir):
    copy('тест-фајлови/tsv/drugitip.tsv', tmpdir)
    путања = Path(tmpdir).joinpath('drugitip.tsv')
    т = tsv.Табела(путања, Елемент)
    тт = са_диска(т)
    with pytest.raises(tsv.ЗаглављеГрешка):
        т.додај(ЕЛЕМЕНТИ)
    with pytest.raises(tsv.ЗаглављеГрешка):
        тт.додај(ЕЛЕМЕНТИ)

