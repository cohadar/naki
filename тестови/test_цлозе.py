import pytest
from каталог.извори.de_cloze import ЦлозеГрешка, формат_уклони_болд, формат_цлозе_питање, формат_цлозе_одговор


def test_формат_уклони_болд():
    assert формат_уклони_болд('trla [[baba]] [lan]') == 'trla [[baba]] lan'


def test_формат_цлозе_питање():
    assert формат_цлозе_питање('u {kom gradu:Beogradu} rođen') == 'u {{{kom gradu}}} rođen'


def test_формат_цлозе_питање_болд_игнориши():
    assert формат_цлозе_питање('trla [baba] {biljka:lan}') == 'trla baba {{{biljka}}}'


def test_формат_цлозе_питање_грешка():
    with pytest.raises(ЦлозеГрешка):
        формат_цлозе_питање('u Beogradu rođen')


def test_формат_цлозе_одговор():
    assert формат_цлозе_одговор('u {kom gradu:Beogradu} rođen') == 'u {Beogradu} rođen'


def test_формат_цлозе_одговор_празан():
    assert формат_цлозе_одговор('aaa {bbb:} ccc') == 'aaa ccc'
    assert формат_цлозе_одговор('aaa {bbb:}ccc') == 'aaa ccc'
    assert формат_цлозе_одговор('aaa {bbb:}') == 'aaa '


def test_формат_цлозе_одговор_болд():
    assert формат_цлозе_одговор('trla [baba] {biljka:lan}') == 'trla [baba] {lan}'


def test_формат_цлозе_одговор_грешка():
    with pytest.raises(ЦлозеГрешка):
        формат_цлозе_одговор('u Beogradu rođen')
