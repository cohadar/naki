from datetime import date, timedelta
from наки.ид import assert_ид
from наки.команда import КОМАНДА_ПРЕКИД, КОМАНДА_ОТВОРИ_УРЛ, КОМАНДА_ЕДИТУЈ
from наки.команда import КОМАНДА_ФЕЈЛ, КОМАНДА_ПЛУС1, КОМАНДА_ПЛУС2


class Шпил():
    def __init__(бре, ui, дир, п_интервала, п_карти, п_линкова, п_записа):
        бре._ui = ui
        бре._дир = дир
        бре.п_интервала = п_интервала
        бре.п_записа = п_записа
        бре.п_линкова = п_линкова
        бре.п_карти = п_карти
        бре.неодрађене = set(карта.ид for карта in бре.п_карти)
        бре.промашене = set()
        бре.прекид = False
        бре.понови_питање = True
        бре.понови_одговор = True
        регистар_питање = бре._ui.регистар_питање
        регистар_питање.региструј(КОМАНДА_ПРЕКИД, бре.а_прекид)
        регистар_питање.региструј(КОМАНДА_ОТВОРИ_УРЛ, бре.а_отвори_урл, урл=None)
        регистар_питање.региструј(КОМАНДА_ЕДИТУЈ, бре.а_измени, извор=None, линија=None)
        регистар_одговор = бре._ui.регистар_одговор
        регистар_одговор.региструј(КОМАНДА_ПРЕКИД, бре.а_прекид)
        регистар_одговор.региструј(КОМАНДА_ОТВОРИ_УРЛ, бре.а_отвори_урл, урл=None)
        регистар_одговор.региструј(КОМАНДА_ЕДИТУЈ, бре.а_измени, извор=None, линија=None)
        регистар_одговор.региструј(КОМАНДА_ФЕЈЛ, бре.а_оцена, ид=None, оцена=0)
        регистар_одговор.региструј(КОМАНДА_ПЛУС1, бре.а_оцена, ид=None, оцена=1)
        регистар_одговор.региструј(КОМАНДА_ПЛУС2, бре.а_оцена, ид=None, оцена=2)

    def може_данас(бре, индекс, ид, врста_карте):
        данас = date.today()
        дп = бре.п_записа.датум_прегледа(ид)
        индекс_интервала = бре.п_записа.индекс_интервала(ид)
        период = бре.п_интервала.период_интервала(врста_карте, индекс_интервала)
        ни = timedelta(days=период)
        return данас > дп + ни

    def припреми(бре):
        бре.п_интервала.консолидуј(бре.п_карти.скуп_врста_карте)
        бре.п_карти.филтрирај(бре.може_данас)
        бре.п_карти.рандомизуј()
        бре.неодрађене = set(карта.ид for карта in бре.п_карти)
        бре.промашене = set()

    def а_прекид(бре):
        бре.прекид = True
        бре.понови_питање = False
        бре.понови_одговор = False

    def а_оцена(бре, ид, оцена):
        бре.оцена(ид, оцена)

    def а_отвори_урл(бре, урл):
        бре._ui.отвори_урл(урл)

    def а_измени(бре, извор, линија):
        права_путања = бре._дир.parent.joinpath(извор)
        бре._ui.измени(права_путања, линија)

    def __len__(бре):
        return len(бре.п_карти)

    def __iter__(бре):
        return iter(бре.п_карти)

    def clear(бре):
        бре.п_карти.clear()

    def урл(бре, ид):
        return бре.п_линкова.линк(ид)

    def оцена(бре, ид, оцена):
        бре.понови_одговор = False
        try:
            assert_ид(ид)
            assert оцена in [0, 1, 2], f"инвалидна оцена: {оцена}"
            бре.п_записа.додај_нови_интервал(ид, оцена)
            бре.неодрађене.discard(ид)
            if оцена > 0:
                бре.промашене.discard(ид)
            else:
                бре.промашене.add(ид)
        except AssertionError as e:
            raise AssertionError(бре.име()) from e

    def име(бре):
        return бре._дир.name

    def преполови(бре):
        def филтер(индекс, ид, врста_карте):
            return индекс % 2 == 0
        бре.п_карти.филтрирај(филтер)
        бре.припреми()

    def избаци_промашене(бре):
        def филтер(индекс, ид, врста_карте):
            return бре.п_записа.промашена(ид)
        бре.п_карти.филтрирај(филтер)
        бре.припреми()

    def задржи_само_промашене(бре):
        def филтер(индекс, ид, врста_карте):
            return not бре.п_записа.промашена(ид)
        бре.п_карти.филтрирај(филтер)
        бре.припреми()

    def сиже(бре):
        return (len(бре.неодрађене), len(бре.промашене))

    def __call__(бре):
        for карта in бре.п_карти:
            ид = карта.ид
            урл = бре.урл(ид)
            број_карата = f"{len(бре.неодрађене)}+{len(бре.промашене)}"
            наслов = карта.врста_карте
            питање = карта.питање
            одговор = карта.одговор
            извор = карта.извор
            линија = карта.линија
            дата = {
                "ид": ид,
                "врста_карте": наслов,
                "урл": урл,
                "извор": извор,
                "линија": линија,
            }
            бре.понови_питање = True
            бре.понови_одговор = True
            while бре.понови_питање:
                покажи_одговор = бре._ui.питање(дата, наслов, питање, број_карата)
                if покажи_одговор:
                    break
            if бре.прекид:
                break
            while бре.понови_одговор:
                бре._ui.одговор(дата, наслов, питање, одговор, број_карата)
            if бре.прекид:
                break
        бре.clear()
        return бре.сиже()

