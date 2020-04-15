import pytest
from наки import tsv
from enum import IntEnum, unique
from pathlib import Path
from shutil import copy
from тест import фајл_хеш
from collections import namedtuple


@unique
class Колоне(IntEnum):
    ИД = 0
    ДАТУМ = 1
    ИНФИНИТИВ = 2
    ПРЕЗЕНТ = 3
    ПРЕТЕРИТ = 4
    ПЕРФЕКТ = 5
    ПРЕВОД = 6


ТипКолоне = namedtuple('ТипКолоне', ['ИД', 'ДАТУМ', 'ИНФИНИТИВ', 'ПРЕЗЕНТ', 'ПРЕТЕРИТ', 'ПЕРФЕКТ', 'ПРЕВОД'])


@unique
class КолонеПогрешнаВеличина(IntEnum):
    ИД = 0
    ДАТУМ = 1
    ИНФИНИТИВ = 2
    ПРЕЗЕНТ = 3
    ПРЕТЕРИТ = 4
    ПЕРФЕКТ = 5


@unique
class КолонеПогрешноИме(IntEnum):
    ИД = 0
    ДАТУМ = 1
    ИНФИНИТИВ = 2
    ПРЕЗЕНТЛАЛАЛА = 3
    ПРЕТЕРИТ = 4
    ПЕРФЕКТ = 5
    ПРЕВОД = 6


def test_учитај_фајл():
    path = Path('тест-фајлови/tsv/ok10.tsv')
    rows = tsv.учитај_фајл(path, Колоне)
    assert len(rows) == 10


def test_учитај():
    путања = Path('тест-фајлови/tsv/ok10.tsv')
    редови = tsv.учитај(путања, ТипКолоне)
    assert len(редови) == 10
    for ред in редови:
        assert isinstance(ред, ТипКолоне)


def test_учитај_фајл_КолонеПогрешнаВеличина():
    path = Path('тест-фајлови/tsv/ok10.tsv')
    with pytest.raises(tsv.КолонеПогрешнаВеличинаГрешка):
        tsv.учитај_фајл(path, КолонеПогрешнаВеличина)


def test_учитај_фајл_КолонеИменаСеНеПоклапају():
    path = Path('тест-фајлови/tsv/ok10.tsv')
    with pytest.raises(tsv.КолонеИменаСеНеПоклапајуГрешка):
        tsv.учитај_фајл(path, КолонеПогрешноИме)


РЕДОВИ = [
    ['4157813edfb24ffc952f1bd9ccf1d9b6', '2019-12-07',
        'dürfen', 'darf', 'durfte', 'hat gedurft', 'smeti'],
    ['f8924411091446248d30895d161966fb', '2019-12-07',
        'empfehlen', 'empfiehlt', 'empfahl', 'hat empfohlen', 'preporučiti'],
]


def test_додај_на_фајл_постоји(tmpdir):
    copy('тест-фајлови/tsv/ok08.tsv', tmpdir)
    path = Path(tmpdir).joinpath('ok08.tsv')
    tsv.додај_на_фајл(path, Колоне, РЕДОВИ)
    assert фајл_хеш('тест-фајлови/tsv/ok10.tsv') == фајл_хеш(path)


def test_додај_на_фајл_непостоји(tmpdir):
    path = Path(tmpdir).joinpath('ok_ново.tsv')
    tsv.додај_на_фајл(path, Колоне, РЕДОВИ)
    assert фајл_хеш('тест-фајлови/tsv/ok02.tsv') == фајл_хеш(path)


def test_додај_на_фајл_КолонеПогрешнаВеличина(tmpdir):
    copy('тест-фајлови/tsv/ok10.tsv', tmpdir)
    path = Path(tmpdir).joinpath('ok10.tsv')
    with pytest.raises(tsv.КолонеПогрешнаВеличинаГрешка):
        tsv.додај_на_фајл(path, КолонеПогрешнаВеличина, РЕДОВИ)


def test_додај_на_фајл_КолонеИменаСеНеПоклапају(tmpdir):
    copy('тест-фајлови/tsv/ok10.tsv', tmpdir)
    path = Path(tmpdir).joinpath('ok10.tsv')
    with pytest.raises(tsv.КолонеИменаСеНеПоклапајуГрешка):
        tsv.додај_на_фајл(path, КолонеПогрешноИме, РЕДОВИ)


def test_препиши_фајл_нови(tmpdir):
    copy('тест-фајлови/tsv/ok10.tsv', tmpdir)
    фајл1 = Path(tmpdir).joinpath('ok10.tsv')
    фајл2 = Path(tmpdir).joinpath('ok10_нови.tsv')
    rows = tsv.учитај_фајл(фајл1, Колоне)
    tsv.препиши_фајл(фајл2, Колоне, rows)
    assert фајл_хеш(фајл1) == фајл_хеш(фајл2)


def test_препиши_фајл_постојећи(tmpdir):
    copy('тест-фајлови/tsv/ok10.tsv', tmpdir)
    copy('тест-фајлови/tsv/ok02.tsv', tmpdir)
    фајл1 = Path(tmpdir).joinpath('ok10.tsv')
    фајл2 = Path(tmpdir).joinpath('ok02.tsv')
    assert фајл_хеш(фајл1) != фајл_хеш(фајл2)
    rows = tsv.учитај_фајл(фајл1, Колоне)
    tsv.препиши_фајл(фајл2, Колоне, rows)
    assert фајл_хеш(фајл1) == фајл_хеш(фајл2)
