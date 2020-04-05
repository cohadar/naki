from pathlib import Path
from наки.вежбање import Вежбање
from наки.терминал import Терминал
from наки.карте import Шпил
from тест import СировиТерминал, ТестШпилДиск
from наки.команда import КОД_СПЕЈС
from наки.команда import КОД_ЦИР_К
from наки.команда import КОД_ЦИР_Е
from наки.команда import КОД_ЦИР_О
# ТЕСТ_КАТАЛОГ = Path(__file__).parent.parent.joinpath('тест-фајлови', 'каталог')

ПУН_ШПИЛ = 100


def вв():
    return Вежбање(Path('каталог'), Шпил(ТестШпилДиск('meh', ПУН_ШПИЛ)))


def тт(кодови):
    return Терминал(СировиТерминал(кодови))


def test_одради_све():
    т = тт([КОД_СПЕЈС] * 10000)
    в = вв()
    assert len(в) == ПУН_ШПИЛ
    неодрађене, промашене = в(т)
    assert len(в) == 0
    assert неодрађене == 0
    assert промашене == 0


def test_изађи_одмах():
    т = тт([КОД_ЦИР_К])
    в = вв()
    assert len(в) == ПУН_ШПИЛ
    неодрађене, промашене = в(т)
    assert len(в) == 0
    assert неодрађене == ПУН_ШПИЛ
    assert промашене == 0


def test_едит_на_питању():
    т = тт([КОД_ЦИР_Е, КОД_ЦИР_К])
    в = вв()
    assert len(в) == ПУН_ШПИЛ
    неодрађене, промашене = в(т)
    assert len(в) == 0
    assert неодрађене == ПУН_ШПИЛ
    assert промашене == 0
    assert len(т.т.измене) == 1


def test_едит_на_одговору():
    т = тт([КОД_СПЕЈС, КОД_ЦИР_Е, КОД_ЦИР_К])
    в = вв()
    assert len(в) == ПУН_ШПИЛ
    неодрађене, промашене = в(т)
    assert len(в) == 0
    assert неодрађене == ПУН_ШПИЛ
    assert промашене == 0
    assert len(т.т.измене) == 1


def test_линк_на_питању():
    т = тт([КОД_ЦИР_О, КОД_ЦИР_К])
    в = вв()
    assert len(в) == ПУН_ШПИЛ
    неодрађене, промашене = в(т)
    assert len(в) == 0
    assert неодрађене == ПУН_ШПИЛ
    assert промашене == 0
    assert len(т.т.отварања) == 1


def test_линк_на_одговору():
    т = тт([КОД_СПЕЈС, КОД_ЦИР_О, КОД_ЦИР_К])
    в = вв()
    assert len(в) == ПУН_ШПИЛ
    неодрађене, промашене = в(т)
    assert len(в) == 0
    assert неодрађене == ПУН_ШПИЛ
    assert промашене == 0
    assert len(т.т.отварања) == 1
