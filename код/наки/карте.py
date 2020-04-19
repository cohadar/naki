import sys
from наки import tsv
from random import shuffle
from collections import defaultdict, namedtuple


Карта = namedtuple('Карта', ['ид', 'врста_карте', 'питање', 'одговор', 'извор', 'линија'])
Карта = tsv.namedtuple(Карта)


class ПогледКарти():
    def __init__(бре, табела):
        бре._табела = табела
        бре._табела.учитај()
        бре._активне = [к for к in бре._табела]
        бре.скуп_врста_карте = set()
        for карта in бре._активне:
            бре.скуп_врста_карте.add(карта.врста_карте)
        нађено = False
        дупло = set()
        идјеви = set()
        for карта in бре._активне:
            ид = карта.ид
            if ид in идјеви:
                raise ValueError(f"дупли ид: {ид}")
            идјеви.add(ид)
            питање = f"{карта.врста_карте}: {карта.питање}"
            if питање in дупло:
                print(f"ДУПЛИКАТ: {питање}", file=sys.stderr)
                нађено = True
            дупло.add(питање)
        if нађено:
            raise ValueError("ДУПЛИКАТИ")
        бре._активне = sorted(бре._активне, key=lambda к: к.врста_карте)

    def филтрирај(бре, филтер):
        бре._активне = [
            карта for и, карта in enumerate(бре._активне)
            if филтер(и, карта.ид, карта.врста_карте)
        ]

    def рандомизуј(бре):
        по_врсти = defaultdict(list)
        for карта in бре._активне:
            врста = карта.врста_карте
            по_врсти[врста].append(карта)
        темп = []
        for в in по_врсти.values():
            shuffle(в)
            темп.extend(в)
        бре._активне = темп

    def __len__(бре):
        return len(бре._активне)

    def __iter__(бре):
        return iter(бре._активне)

    def clear(бре):
        бре._активне.clear()

    def стат_скуп_идјева(бре):
        return set(к.ид for к in бре._табела)

