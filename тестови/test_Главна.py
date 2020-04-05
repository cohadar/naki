from pathlib import Path
from наки.__main__ import Главна
from contextlib import contextmanager

ПУТАЊА_КАТАЛОГА = Path(__file__).parent.parent.joinpath('тест-фајлови', 'каталог')


def тест_шпилови():
    return [
        ('тест_сви_одрађени', 5),
        ('тест_без_записа_и_линкова', 40),
        ('тест_без_линкова', 61),
        ('тест_одрађено_пола', 93),
        ('тест_без_записа', 95),
        ('тест_сви_неодрађени', 102),
    ]


class ТестТерминал():
    def __init__(бре, команде):
        бре.команде = команде
        бре.и = iter(команде)

    def инпут(бре, *args):
        return next(бре.и)

    def обриши(*args):
        pass

    @contextmanager
    def статус(бре, *args):
        try:
            yield 117
        finally:
            pass

    @contextmanager
    def главни(бре, *args):
        try:
            yield 217
        finally:
            pass

    def принт_сепаратор(бре, *args):
        pass

    def принт(бре, *args):
        pass


def test_Главна_изађи_одмах():
    тт = ТестТерминал(['к'])
    г = Главна(тт, ПУТАЊА_КАТАЛОГА)
    шпилови = г()
    assert шпилови == тест_шпилови()
