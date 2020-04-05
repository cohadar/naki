from contextlib import contextmanager


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
