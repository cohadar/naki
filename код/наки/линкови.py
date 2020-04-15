from enum import unique, IntEnum
# from collections import namedtuple
from наки.ид import assert_ид, извор_ид


@unique
class ЛинкЕнум(IntEnum):
    ИД = 0
    УРЛ = 1


# Линк = namedtuple('Линк', ['ид', 'урл'])


class ФајлЛинкова():
    def __init__(бре, tsv, путања, сирови_линкови):
        бре._tsv = tsv
        бре._сирови_линкови = сирови_линкови
        бре._путања = путања
        бре._линк_мапа = {}
        for л in сирови_линкови:
            ид = л[ЛинкЕнум.ИД]
            урл = л[ЛинкЕнум.УРЛ]
            assert_ид(ид)
            if ид in бре._линк_мапа:
                raise ValueError(f"Дупли линк ид: {ид}")
            бре._линк_мапа[ид] = урл

    @staticmethod
    def учитај(tsv, путања):
        сирови_линкови = tsv.учитај_фајл(путања, ЛинкЕнум) if путања.exists() else []
        return ФајлЛинкова(tsv, путања, сирови_линкови)

    def линк(бре, ид):
        урл = бре._линк_мапа.get(ид, None)
        if not урл:
            урл = бре._линк_мапа.get(извор_ид(ид), None)
        return урл
