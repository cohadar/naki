from contextlib import contextmanager


class ТестТерминал():
    def __init__(бре, команде):
        assert type(команде) == list
        for к in команде:
            assert type(к) == str
        бре._и = iter(команде)
        бре.измене = []
        бре.отварања = []
        бре.звукова = 0
        бре._болд = '[bold]'
        бре._плаво = '[blue]'
        бре._нормал = '[/normal]'

    @contextmanager
    def статус(бре):
        try:
            yield 'статус'
        finally:
            pass

    @contextmanager
    def главни(бре):
        try:
            yield 'главни'
        finally:
            pass

    @contextmanager
    def пун_екран(бре):
        try:
            yield 'пун_екран'
        finally:
            pass

    @contextmanager
    def сакривен_курсор(бре):
        try:
            yield 'сакривен_курсор'
        finally:
            pass

    def инпут(бре, текст):
        return next(бре._и)

    def инпут_код(бре):
        return next(бре._и)

    def формат_мд(бре, текст):
        return текст

    def обриши(бре):
        pass

    def принт(бре, *args, **kw):
        pass

    def принт_сиво(бре, текст):
        pass

    def принт_плаво(бре, текст):
        pass

    def принт_зелено(бре, текст):
        pass

    def отвори_урл(бре, урл):
        бре.отварања.append(урл)

    def измени(бре, права_путања, линија):
        бре.измене.append((права_путања, линија))

    def додај_на_извор(бре, путања):
        pass

    def звук_грешке(бре):
        бре.звукова += 1

