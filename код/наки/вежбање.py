from наки.команда import КОМАНДА_ПРЕКИД, КОМАНДА_ОТВОРИ_УРЛ, КОМАНДА_ЕДИТУЈ
from наки.команда import КОМАНДА_ФЕЈЛ, КОМАНДА_ПЛУС1, КОМАНДА_ПЛУС2
from наки.карте import Карта


def измени(терминал, путања_каталога, лепа_путања, линија):
    права_путања = путања_каталога.joinpath(лепа_путања)
    терминал.измени(права_путања, линија)


def питање_и_одговор(терминал, путања_каталога, карта, број_преосталих_карата, урл):
    терминал.обриши()
    with терминал.главни():
        терминал.принт_наслов(карта[Карта.ВРСТА_КАРТЕ.value])
        терминал.принт_мд(карта[Карта.ПИТАЊЕ.value])
        терминал.принт_сепаратор('-')
        with терминал.статус():
            терминал.принт_сепаратор('=', број_преосталих_карата)
            терминал.принт('притисни било који тастер')
        while True:
            к = терминал.инпут_код()
            if к in КОМАНДА_ПРЕКИД:
                return (True, None)
            if к in КОМАНДА_ОТВОРИ_УРЛ:
                if урл:
                    терминал.отвори_урл(урл)
                else:
                    терминал.звук_грешке()
                continue
            if к in КОМАНДА_ЕДИТУЈ:
                измени(терминал, путања_каталога, карта[Карта.ИЗВОР.value], карта[Карта.ЛИНИЈА.value])
                continue
            break
        терминал.принт_мд(карта[Карта.ОДГОВОР.value])
        with терминал.статус():
            терминал.принт_сепаратор('=', број_преосталих_карата)
            терминал.принт('оцени одговор (f: 0)(space: +1)(enter: +2)')
        ДОЗВОЉЕНЕ = [КОМАНДА_ПРЕКИД, КОМАНДА_ОТВОРИ_УРЛ, КОМАНДА_ЕДИТУЈ, КОМАНДА_ФЕЈЛ, КОМАНДА_ПЛУС1, КОМАНДА_ПЛУС2]

        def екстра(и):
            for к in ДОЗВОЉЕНЕ:
                if и in к:
                    return к
            return None

        while True:
            к = терминал.инпут_код(екстра)
            if к in КОМАНДА_ПРЕКИД:
                return (True, None)
            elif к in КОМАНДА_ОТВОРИ_УРЛ:
                if урл:
                    терминал.отвори_урл(урл)
                else:
                    терминал.звук_грешке()
                continue
            elif к in КОМАНДА_ЕДИТУЈ:
                измени(терминал, путања_каталога, карта[Карта.ИЗВОР.value], карта[Карта.ЛИНИЈА.value])
                continue
            elif к in КОМАНДА_ФЕЈЛ:
                return (False, 0)
            elif к in КОМАНДА_ПЛУС1:
                return (False, 1)
            elif к in КОМАНДА_ПЛУС2:
                return (False, 2)
            else:
                raise Exception(f'непозната команда: {к}')


class Вежбање():
    def __init__(бре, путања_каталога, шпил):
        бре.шпил = шпил
        бре.путања_каталога = путања_каталога
        бре.неодрађене = set(карта[Карта.ИД] for карта in бре.шпил)
        бре.промашене = set()

    def име_шпила(бре):
        return бре.шпил.име()

    def __len__(бре):
        return len(бре.шпил)

    def __call__(бре, терминал):
        бре.шпил.рандомизуј()
        for карта in бре.шпил:
            ид = карта[Карта.ИД]
            урл = бре.шпил.урл(ид)
            број_карата = f"{len(бре.неодрађене)}+{len(бре.промашене)}"
            прекид, оцена = питање_и_одговор(терминал, бре.путања_каталога, карта, број_карата, урл)
            if прекид:
                break
            бре.шпил.оцена(ид, оцена)
            бре.неодрађене.discard(ид)
            if оцена > 0:
                бре.промашене.discard(ид)
            else:
                бре.промашене.add(ид)
        бре.шпил.clear()
        return бре.сиже()

    def преполови(бре):
        бре.шпил.преполови()

    def избаци_промашене(бре):
        бре.шпил.избаци_промашене()

    def сиже(бре):
        return (len(бре.неодрађене), len(бре.промашене))
