import time
import uuid
import random
from наки.карте import Карта


def идијеви(брј):
    assert 0 < брј and брј <= 16
    основа = uuid.uuid4().hex[:-1]
    рет = []
    for и in iter(range(брј)):
        хкс = hex(и)[-1]
        рет.append(основа + хкс)
    return рет


СЛОВА = 'љњертзуиопшђасдфгхјклчћжѕџцвбнмЉЊЕРТЗУИОПШЂАСДФГХЈКЛЧЋЖЅЏЦВБНМ'
ЗНАЦИ = r'\,.?!()[]{}'


def реч(доња, горња, екстра=None):
    дужина = random.randint(доња, горња)
    рет = ''
    for и in range(дужина):
        if екстра:
            рет += random.choice(СЛОВА + екстра)
        else:
            рет += random.choice(СЛОВА)
    return рет


def речи(брј):
    return [реч(3, 15) for _ in range(брј)]


def реченица():
    дужина = random.randint(2, 10)
    речи = [реч(3, 15, ЗНАЦИ) for _ in range(дужина)]
    return ' '.join(речи)


def врста_карте():
    а = реч(3, 15)
    б = реч(3, 15)
    return f'{а} <= {б}'.upper()


def извор():
    а = реч(3, 15)
    б = реч(3, 15)
    ц = реч(3, 15)
    return f'{а}/{б}/{ц}.tsv'


def линија():
    return random.randint(1, 1000)


def карте(брј):
    рет = []
    број_врста_карте = max(1, брј // 5)
    вк = [врста_карте() for _ in range(број_врста_карте)]
    while len(рет) < брј:
        for ид in идијеви(random.randint(1, 16)):
            рет.append(Карта(ид, random.choice(вк), реченица(), реченица(), извор(), линија()))
    return рет[:брј]


def main():
    for карта in карте(5):
        print(карта)


if __name__ == '__main__':
    main()

# def направи_линк(извор):
#     ид = извор[Извор.ИД]
#     питање = 'ли' + str(random.random())[2:]
#     return [ид, f"https://www.google.de/search?tbm=isch&q={питање}"]


# def извор_одради(лепа_путања, извор):
#     карте = []
#     индекс = iter(range(16))

#     # 0, 1
#     def питање(џ):
#         return 'пи' + str(random.random())[2:]

#     def одговор(џ):
#         return 'од' + str(random.random())[2:]

#     for и in range(1, random.randint(1, 16)):
#         карте.extend(направи_карте(лепа_путања, извор, f"ТИП{и}", питање, одговор, next(индекс)))
#     линкови = [направи_линк(и) for и in извор]
#     return карте, линкови


# def _рандом_датум():
#     пет_година = 60*60*24*365*5
#     данас = time.mktime(time.localtime())
#     датум = time.localtime(данас - random.randint(0, пет_година))
#     return time.strftime("%Y-%m-%d", датум)


# def извор_учитај(путања):
#     рез = []
#     for _ in range(random.randint(5, 10)):
#         рез.append([
#             uuid.uuid4().hex[:-1] + '0',
#             _рандом_датум(),
#             'ле' + str(random.random())[2:],
#             'де' + str(random.random())[2:],
#         ])
#     return рез
