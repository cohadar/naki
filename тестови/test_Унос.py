from наки.унос import Унос, Главна
from наки.ui import UI
from pathlib import Path
from тест import ТестТерминал
from наки.команда import КОД_ЦИР_К


def ту(име):
    return Унос(Path(име))


def тест_уноси():
    return [
        ту('aaa'),
        ту('bbb'),
        ту('ccc'),
        ту('ddd'),
    ]


def главна(команде):
    return Главна(UI(ТестТерминал(команде)), тест_уноси())()


def test_изађи_одмах():
    рез = главна([КОД_ЦИР_К])
    assert рез == [0, 0, 0, 0]


def test_унеси_неколико():
    рез = главна(['2'] + (['3'] * 7) + [КОД_ЦИР_К])
    assert рез == [0, 1, 7, 0]
