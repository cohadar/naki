from collections import namedtuple
from наки.ид import assert_ид, извор_ид


Линк = namedtuple('Линк', ['ид', 'урл'])


class ТабелаЛинкова():
    def __init__(бре, tsv, путања):
        бре._tsv = tsv
        бре._путања = путања
        бре._елементи = []

    def учитај(бре):
        бре._елементи.extend(бре._tsv.учитај(бре._путања, бре))

    def додај(бре, елементи):
        бре._елементи.extend(елементи)
        бре._tsv.додај(бре._путања, бре, елементи)

    def __len__(бре):
        return len(бре._елементи)

    def __iter__(бре):
        return iter(бре._елементи)

    def заглавље(бре):
        return [п.upper() for п in Линк._fields]

    def ред(бре, елемент):
        return list(елемент)

    def елемент(бре, ред):
        return Линк(*ред)


class ПогледЛинкова():
    def __init__(бре, табела):
        бре._табела = табела
        бре._линк_мапа = {}
        бре._табела.учитај()
        for л in табела:
            assert_ид(л.ид)
            if л.ид in бре._линк_мапа:
                raise ValueError(f"Дупли линк ид: {л.ид}")
            бре._линк_мапа[л.ид] = л.урл

    def линк(бре, ид):
        урл = бре._линк_мапа.get(ид, None)
        if not урл:
            урл = бре._линк_мапа.get(извор_ид(ид), None)
        return урл

