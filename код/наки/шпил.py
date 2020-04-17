from datetime import date, timedelta
from наки import tsv
from наки.интервали import ФајлИнтервала
from наки.запис import ПогледЗаписа, ТабелаЗаписа
from наки.линкови import ФајлЛинкова
from наки.карте import ФајлКарти
from наки.ид import assert_ид


class Шпил():
    def __init__(бре, име, фајл_интервала, фајл_карти, фајл_линкова, фајл_записа):
        бре._име = име
        бре.фајл_интервала = фајл_интервала
        бре.фајл_записа = фајл_записа
        бре.фајл_линкова = фајл_линкова
        бре.фајл_карти = фајл_карти

    @staticmethod
    def учитај(дир):
        фајл_интервала = ФајлИнтервала.учитај(tsv, дир.joinpath('интервали.tsv'))
        фајл_карти = ФајлКарти.учитај(tsv, дир.joinpath('карте.tsv'))
        фајл_записа = ПогледЗаписа(ТабелаЗаписа(дир.joinpath('запис.tsv')))
        фајл_линкова = ФајлЛинкова.учитај(tsv, дир.joinpath('линкови.tsv'))

        return Шпил(дир.name, фајл_интервала, фајл_карти, фајл_линкова, фајл_записа)

    def може_данас(бре, индекс, ид, врста_карте):
        данас = date.today()
        дп = бре.фајл_записа.датум_прегледа(ид)
        индекс_интервала = бре.фајл_записа.индекс_интервала(ид)
        период = бре.фајл_интервала.период_интервала(врста_карте, индекс_интервала)
        ни = timedelta(days=период)
        return данас > дп + ни

    def припреми(бре):
        бре.фајл_интервала.консолидуј(бре.фајл_карти.скуп_врста_карте)
        бре.фајл_карти.филтрирај(бре.може_данас)
        бре.фајл_карти.рандомизуј()

    def __len__(бре):
        return len(бре.фајл_карти)

    def __iter__(бре):
        return iter(бре.фајл_карти)

    def clear(бре):
        бре.фајл_карти.clear()

    def урл(бре, ид):
        return бре.фајл_линкова.линк(ид)

    def оцена(бре, ид, врста_карте, оцена):
        try:
            assert_ид(ид)
            assert оцена in [0, 1, 2], f"инвалидна оцена: {оцена}"
            макс_интервал = бре.фајл_интервала.макс_интервал(врста_карте)
            бре.фајл_записа.додај_нови_интервал(ид, оцена, макс_интервал)
        except AssertionError as e:
            raise AssertionError(бре._име, e)

    def име(бре):
        return бре._име

    def преполови(бре):
        def филтер(индекс, ид, врста_карте):
            return индекс % 2 == 0
        бре.фајл_карти.филтрирај(филтер)

    def избаци_промашене(бре):
        def филтер(индекс, ид, врста_карте):
            return бре.фајл_записа.промашена(ид)
        бре.фајл_карти.филтрирај(филтер)

    def задржи_само_промашене(бре):
        def филтер(индекс, ид, врста_карте):
            return not бре.фајл_записа.промашена(ид)
        бре.фајл_карти.филтрирај(филтер)

