from pathlib import Path
from наки.вежбање import Вежбање
from тест import ТестТерминал, ТестШпил
from наки.команда import КОМАНДА_ПЛУС1

ТЕСТ_КАТАЛОГ = Path(__file__).parent.parent.joinpath('тест-фајлови', 'каталог')


def test_одради_све():
    тт = ТестТерминал([КОМАНДА_ПЛУС1] * 10000)
    в = Вежбање(ТестШпил('тест_без_записа', 100))
    assert len(в) == 100
    в(тт)
    assert len(в) == 0
