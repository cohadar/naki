from наки.__main__ import Главна
from наки.вежбање import Вежбање
from наки.терминал import Терминал
from наки.карте import Шпил
from наки.ui import UI
from тест import СировиТерминал, шпил_лоадер
from наки.команда import КОД_ЦИР_К
from наки.команда import КОД_ЦИР_П
from наки.команда import КОД_ЦИР_И
from наки.команда import КОД_СПЕЈС
from наки.команда import КОД_ЕНТЕР


ОДРАЂЕНО = 0


def тв(име, лен):
    return Вежбање('каталог', Шпил(**шпил_лоадер(име, лен)))


def тест_вежбања():
    return [
        тв('aaa', 0),
        тв('bbb', 5),
        тв('ccc', 10),
        тв('ddd', 15),
    ]


def главна(команде):
    return Главна(UI(Терминал(СировиТерминал(команде))), тест_вежбања())()


def test_изађи_одмах():
    рез = главна([КОД_ЦИР_К])
    assert рез == [
        (0, 0),
        (5, 0),
        (10, 0),
        (15, 0),
    ]


# def test_преполови():
#     рез = главна([КОД_ЦИР_П, КОД_ЦИР_К])
#     for a, б in zip(рез, тест_вежбања()):
#         assert a.име_шпила() == б.име_шпила()
#         assert len(a) == (len(б) + 1) // 2


# def test_избаци_промашене():
#     рез = главна([КОД_ЦИР_И, КОД_ЦИР_К])
#     for a, б in zip(рез, тест_вежбања()):
#         assert a.име_шпила() == б.име_шпила()
#         assert len(a) == max(0, len(б) - 2)


# def test_одради_цео_шпил():
#     рез = главна(['2'] + ([КОД_СПЕЈС] * 10) + [КОД_ЦИР_К])
#     assert рез == [
#         тв('aaa', 0),
#         тв('bbb', ОДРАЂЕНО),
#         тв('ccc', 10),
#         тв('ddd', 15),
#     ]


# def test_одради_двe_карте():
#     рез = главна(['2'] + ([КОД_СПЕЈС] * 2) + [КОД_ЦИР_К] * 2)
#     assert рез == [
#         тв('aaa', 0),
#         тв('bbb', ОДРАЂЕНО),
#         тв('ccc', 10),
#         тв('ddd', 15),
#     ]


# def test_одради_два_шпила():
#     рез = главна(['2'] + ([КОД_СПЕЈС] * 10) + ['3'] + ([КОД_ЕНТЕР] * 20) + [КОД_ЦИР_К])
#     assert рез == [
#         тв('aaa', 0),
#         тв('bbb', ОДРАЂЕНО),
#         тв('ccc', ОДРАЂЕНО),
#         тв('ddd', 15),
#     ]
