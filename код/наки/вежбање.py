from наки.карте import Карта
from наки.команда import Регистар, КОМАНДА_ПРЕКИД, КОМАНДА_ОТВОРИ_УРЛ, КОМАНДА_ЕДИТУЈ
from наки.команда import КОМАНДА_ФЕЈЛ, КОМАНДА_ПЛУС1, КОМАНДА_ПЛУС2


class Вежбање():
    def _учитај(бре):
        бре.неодрађене = set(карта[Карта.ИД] for карта in бре.шпил)
        бре.промашене = set()

    def __init__(бре, путања_каталога, шпил):
        бре.шпил = шпил
        бре.путања_каталога = путања_каталога
        бре._учитај()
        бре.регистар_питање = Регистар()
        бре.регистар_питање.региструј(КОМАНДА_ПРЕКИД, бре.а_прекид)
        бре.регистар_питање.региструј(КОМАНДА_ОТВОРИ_УРЛ, бре.а_отвори_урл)
        бре.регистар_питање.региструј(КОМАНДА_ЕДИТУЈ, бре.а_измени)
        бре.регистар_одговор = Регистар()
        бре.регистар_одговор.региструј(КОМАНДА_ПРЕКИД, бре.а_прекид)
        бре.регистар_одговор.региструј(КОМАНДА_ОТВОРИ_УРЛ, бре.а_отвори_урл)
        бре.регистар_одговор.региструј(КОМАНДА_ЕДИТУЈ, бре.а_измени)
        бре.регистар_одговор.региструј(КОМАНДА_ФЕЈЛ, бре.а_оцена)
        бре.регистар_одговор.региструј(КОМАНДА_ПЛУС1, бре.а_оцена)
        бре.регистар_одговор.региструј(КОМАНДА_ПЛУС2, бре.а_оцена)
        бре.прекид = False
        бре.понови_питање = True
        бре.понови_одговор = True

    def а_прекид(бре, код, **дата):
        бре.прекид = True
        бре.понови_питање = False
        бре.понови_одговор = False

    def а_отвори_урл(бре, код, ui, урл, **дата):
        ui.отвори_урл(урл)

    def а_измени(бре, код, ui, извор, линија, **дата):
        права_путања = бре.путања_каталога.joinpath(извор)
        ui.измени(права_путања, линија)

    def а_оцена(бре, код, ид, **дата):
        if код in КОМАНДА_ФЕЈЛ:
            оцена = 0
        elif код in КОМАНДА_ПЛУС1:
            оцена = 1
        elif код in КОМАНДА_ПЛУС2:
            оцена = 2
        else:
            raise ValueError(f"Непознат код {код}")
        бре.шпил.оцена(ид, оцена)
        бре.неодрађене.discard(ид)
        if оцена > 0:
            бре.промашене.discard(ид)
        else:
            бре.промашене.add(ид)
        бре.понови_одговор = False

    def име_шпила(бре):
        return бре.шпил.име()

    def __len__(бре):
        return len(бре.шпил)

    def __call__(бре, ui):
        бре.шпил.рандомизуј()
        for карта in бре.шпил:
            ид = карта[Карта.ИД]
            урл = бре.шпил.урл(ид)
            број_карата = f"{len(бре.неодрађене)}+{len(бре.промашене)}"
            наслов = карта[Карта.ВРСТА_КАРТЕ.value]
            питање = карта[Карта.ПИТАЊЕ.value]
            одговор = карта[Карта.ОДГОВОР.value]
            извор = карта[Карта.ИЗВОР.value]
            линија = карта[Карта.ЛИНИЈА.value]
            дата = {
                "ui": ui,
                "ид": ид,
                "урл": урл,
                "извор": извор,
                "линија": линија,
            }
            бре.понови_питање = True
            бре.понови_одговор = True
            while бре.понови_питање:
                покажи_одговор = ui.питање(бре.регистар_питање, дата, наслов, питање, број_карата)
                if покажи_одговор:
                    break
            if бре.прекид:
                break
            while бре.понови_одговор:
                ui.одговор(бре.регистар_одговор, дата, наслов, питање, одговор, број_карата)
            if бре.прекид:
                break
        бре.шпил.clear()
        return бре.сиже()

    def преполови(бре):
        бре.шпил.преполови()
        бре._учитај()

    def избаци_промашене(бре):
        бре.шпил.избаци_промашене()
        бре._учитај()

    def задржи_само_промашене(бре):
        бре.шпил.задржи_само_промашене()
        бре._учитај()

    def сиже(бре):
        return (len(бре.неодрађене), len(бре.промашене))
