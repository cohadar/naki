import pytest
from наки import tsv
from enum import IntEnum, unique
from pathlib import Path
from shutil import copy


@unique
class Колоне(IntEnum):
    ИД = 0
    ДАТУМ = 1
    ИНФИНИТИВ = 2
    ПРЕЗЕНТ = 3
    ПРЕТЕРИТ = 4
    ПЕРФЕКТ = 5
    ПРЕВОД = 6


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


def _линије(путања):
    return open(путања, "r").readlines()


def test_учитај_фајл():
    path = Path('тест-фајлови/tsv/ok10.tsv')
    rows = tsv.учитај_фајл(path, Колоне)
    assert len(rows) == 10


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
    assert _линије('тест-фајлови/tsv/ok10.tsv') == _линије(path)


def test_додај_на_фајл_непостоји(tmpdir):
    path = Path(tmpdir).joinpath('ok_ново.tsv')
    tsv.додај_на_фајл(path, Колоне, РЕДОВИ)
    assert _линије('тест-фајлови/tsv/ok02.tsv') == _линије(path)


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
