from pathlib import Path
from наки.вежбање import Вежбање
from наки.терминал import Терминал
from тест import СировиТерминал, ТестШпил
from наки.команда import КОД_СПЕЈС

# ТЕСТ_КАТАЛОГ = Path(__file__).parent.parent.joinpath('тест-фајлови', 'каталог')


def test_одради_све():
    тт = Терминал(СировиТерминал([КОД_СПЕЈС] * 10000))
    в = Вежбање(ТестШпил('тест_без_записа', 100))
    assert len(в) == 100
    в(тт)
    assert len(в) == 0
