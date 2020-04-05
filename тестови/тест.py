from contextlib import contextmanager


class ТестТерминал():
    def __init__(бре, команде):
        бре.команде = команде
        бре.и = iter(команде)

    def инпут(бре, *args):
        return next(бре.и)

    def унеси_команду(бре, *args):
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

    def принт_наслов(бре, *args):
        pass

    def принт_мд(бре, *args):
        pass


class ТестШпил():
    def __init__(бре, име, лен):
        бре._име = име
        бре._лен = лен
        бре._активне = [f'karta.{бре.име}.{и}' for и in range(1, лен + 1)]

    def __len__(бре):
        return бре._лен

    def рандомизуј(бре, *args):
        pass

    def __iter__(бре):
        return iter(бре._активне)

    def урл(бре, ид):
        return 'https://njak.com/' + ид

    def оцена(бре, ид, оцена):
        бре._лен -= 1

    def clear(бре):
        бре._лен = 0

    def име(бре):
        return бре._име

    def __eq__(бре, други):
        if not isinstance(други, ТестШпил):
            return False
        return бре._активне == други._активне

    def __repr__(бре):
        return f'ТестШпил({бре._име}{бре._лен})'
