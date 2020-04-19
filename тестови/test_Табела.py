import pytest
from наки import tsv
from pathlib import Path
from shutil import copy
from тест import фајл_хеш
from collections import namedtuple


Елемент = namedtuple('Елемент', ['ИД', 'ДАТУМ', 'ИНФИНИТИВ', 'ПРЕЗЕНТ', 'ПРЕТЕРИТ', 'ПЕРФЕКТ', 'ПРЕВОД'])


ЕЛЕМЕНТИ = [
    Елемент('4157813edfb24ffc952f1bd9ccf1d9b6', '2019-12-07',
            'dürfen', 'darf', 'durfte', 'hat gedurft', 'smeti'),
    Елемент('f8924411091446248d30895d161966fb', '2019-12-07',
            'empfehlen', 'empfiehlt', 'empfahl', 'hat empfohlen', 'preporučiti'),
]


class ТабелаЕлемената():
    def __init__(бре, путања, елементи=None):
        бре._путања = путања
        бре._елементи = []
        if елементи:
            бре._елементи.extend(елементи)

    def учитај(бре):
        бре._елементи.extend(tsv.учитај(бре._путања, бре))

    def додај(бре, елементи):
        бре._елементи.extend(елементи)
        tsv.додај(бре._путања, бре, елементи)

    def заглавље(бре):
        return list(Елемент._fields)

    def ред(бре, елемент):
        return list(елемент)

    def елемент(бре, ред):
        return Елемент(*ред)

    def __len__(бре):
        return len(бре._елементи)

    def __iter__(бре):
        return iter(бре._елементи)


def test_учитај_фајл():
    path = Path('тест-фајлови/tsv/ok10.tsv')
    табела = ТабелаЕлемената(path)
    табела.учитај()
    assert len(табела) == 10


def test_учитај_фајл_КолонеПогрешнаВеличина():
    path = Path('тест-фајлови/tsv/tabfali.tsv')
    with pytest.raises(tsv.ПарсирањеГрешка):
        табела = ТабелаЕлемената(path)
        табела.учитај()


def test_учитај_фајл_КолонеИменаСеНеПоклапају():
    path = Path('тест-фајлови/tsv/drugitip.tsv')
    with pytest.raises(tsv.ЗаглављеГрешка):
        табела = ТабелаЕлемената(path)
        табела.учитај()


def test_додај_на_фајл_постоји(tmpdir):
    copy('тест-фајлови/tsv/ok08.tsv', tmpdir)
    path = Path(tmpdir).joinpath('ok08.tsv')
    табела = ТабелаЕлемената(path)
    табела.додај(ЕЛЕМЕНТИ)
    assert фајл_хеш('тест-фајлови/tsv/ok10.tsv') == фајл_хеш(path)


def test_додај_на_фајл_непостоји(tmpdir):
    path = Path(tmpdir).joinpath('ok_ново.tsv')
    табела = ТабелаЕлемената(path)
    табела.додај(ЕЛЕМЕНТИ)
    assert фајл_хеш('тест-фајлови/tsv/ok02.tsv') == фајл_хеш(path)


def test_додај_на_фајл_КолонеИменаСеНеПоклапају(tmpdir):
    copy('тест-фајлови/tsv/drugitip.tsv', tmpdir)
    path = Path(tmpdir).joinpath('drugitip.tsv')
    with pytest.raises(tsv.ЗаглављеГрешка):
        табела = ТабелаЕлемената(path)
        табела.додај(ЕЛЕМЕНТИ)

