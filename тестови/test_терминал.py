from наки.терминал import Терминал


def test_формат_мд_болд():
    т = Терминал(force_styling=True)
    assert т.формат_мд('trla [baba] lan') == f'trla {т.т.bold}baba{т.т.normal} lan'


def test_формат_мд_болд_игнориши():
    т = Терминал(force_styling=True)
    assert т.формат_мд('trla [[baba]] lan') == 'trla [baba] lan'


def test_формат_мд_плаво():
    т = Терминал(force_styling=True)
    assert т.формат_мд('trla {baba} lan') == f'trla {т.т.blue}baba{т.т.normal} lan'


def test_формат_мд_плаво_игнориши():
    т = Терминал(force_styling=True)
    assert т.формат_мд('trla {{baba}} lan') == 'trla {baba} lan'


def test_формат_мд_цлозе():
    т = Терминал(force_styling=True)
    assert т.формат_мд('trla {{{baba}}} lan') == f'trla {т.т.blue}{{baba}}{т.т.normal} lan'


def test_формат_мд():
    т = Терминал(force_styling=True)
    assert т.формат_мд('trla {baba} [lan]') == f'trla {т.т.blue}baba{т.т.normal} {т.т.bold}lan{т.т.normal}'
