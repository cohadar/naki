import pytest
from наки import tsv
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


def test_учитај_фајл():
    path = Path('тест-фајлови/tsv/ok10.tsv')
    табела = tsv.Табела(path, Елемент)
    табела.учитај()
    assert len(табела) == 10


def test_учитај_фајл_идемпотентна():
    path = Path('тест-фајлови/tsv/ok10.tsv')
    табела = tsv.Табела(path, Елемент)
    табела.учитај()
    табела.учитај()
    assert len(табела) == 10


def test_учитај_фајл_рет():
    path = Path('тест-фајлови/tsv/ok10.tsv')
    табела = tsv.Табела(path, Елемент)
    т1 = табела.учитај()
    assert id(т1) == id(табела)


def test_учитај_фајл_КолонеПогрешнаВеличина():
    path = Path('тест-фајлови/tsv/tabfali.tsv')
    with pytest.raises(tsv.ПарсирањеГрешка):
        табела = tsv.Табела(path, Елемент)
        табела.учитај()


def test_учитај_фајл_КолонеИменаСеНеПоклапају():
    path = Path('тест-фајлови/tsv/drugitip.tsv')
    with pytest.raises(tsv.ЗаглављеГрешка):
        табела = tsv.Табела(path, Елемент)
        табела.учитај()


def test_додај_на_фајл_постоји(tmpdir):
    copy('тест-фајлови/tsv/ok08.tsv', tmpdir)
    path = Path(tmpdir).joinpath('ok08.tsv')
    табела = tsv.Табела(path, Елемент)
    табела.додај(ЕЛЕМЕНТИ)
    assert фајл_хеш('тест-фајлови/tsv/ok10.tsv') == фајл_хеш(path)


def test_додај_на_фајл_непостоји(tmpdir):
    path = Path(tmpdir).joinpath('ok_ново.tsv')
    табела = tsv.Табела(path, Елемент)
    табела.додај(ЕЛЕМЕНТИ)
    assert фајл_хеш('тест-фајлови/tsv/ok02.tsv') == фајл_хеш(path)


def test_додај_на_фајл_КолонеИменаСеНеПоклапају(tmpdir):
    copy('тест-фајлови/tsv/drugitip.tsv', tmpdir)
    path = Path(tmpdir).joinpath('drugitip.tsv')
    with pytest.raises(tsv.ЗаглављеГрешка):
        табела = tsv.Табела(path, Елемент)
        табела.додај(ЕЛЕМЕНТИ)

