from collections import namedtuple
from наки.ид import assert_ид, извор_ид


Линк = namedtuple('Линк', ['ид', 'урл'])


def заглавље():
    return [п.upper() for п in Линк._fields]


def ред(елемент):
    return list(елемент)


def елемент(ред):
    return Линк(*ред)


setattr(Линк, 'заглавље', заглавље)
setattr(Линк, 'ред', ред)
setattr(Линк, 'елемент', елемент)


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

