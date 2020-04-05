from contextlib import contextmanager
from blessings import Terminal


class СировиТерминал():
    def __init__(бре, команде):
        assert type(команде) == list
        for к in команде:
            assert type(к) == str
        бре._и = iter(команде)
        бре._т = Terminal()
        бре.height = 48
        бре.width = 170

    @contextmanager
    def location(бре, x, y):
        try:
            yield 'trla baba lan'
        finally:
            pass

    def print(бре, *args, **kw):
        pass

    def input(бре, *args):
        return next(бре._и)

    def readkey(бре, *args):
        return next(бре._и)

    def clear(бре):
        pass

    def __getattr__(бре, атрибут):
        if атрибут in ['color', 'normal', 'green', 'bold', 'blue']:
            рез = getattr(бре._т, атрибут)
            if рез is None:
                raise ValueError(f'nesme none {атрибут}')
            return рез
        raise AttributeError(атрибут)


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
        return бре._име == други._име and бре._лен == други._лен

    def __repr__(бре):
        return f'ТестШпил({бре._име}{бре._лен})'

    def преполови(бре):
        бре._лен = (бре._лен + 1) // 2

    def избаци_промашене(бре):
        бре._лен = max(0, бре._лен - 2)
