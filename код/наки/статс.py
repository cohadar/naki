from наки import tsv
from наки.карте import ФајлКарти
from наки.запис import ПогледЗаписа, ТабелаЗаписа
from наки.конфигурација import ПУТАЊА_КАТАЛОГА


class Статистика:
    def __init__(бре, дир, карте, запис):
        бре.дир = дир
        бре.карте = карте
        бре.запис = запис

    def непогледане(бре):
        к = бре.карте.стат_скуп_идјева()
        з = бре.запис.стат_скуп_идјева()
        return len(к.difference(з))

    def у_интервалу(бре):
        return бре.запис.стат_број_карти_по_интервалу()

    def проценат_промашених(бре):
        бре.запис.стат_проценат_промашених_карти()

    def укупно(бре):
        return len(бре.карте)

    def штампај(бре):
        print('=' * 79)
        print(бре.дир.name)
        print(f"непогледане={бре.непогледане()}")
        print(f"у_интервалу={бре.у_интервалу()}")
        print(f"проценат_промашених={бре.проценат_промашених()}%")
        print(f"укупно={бре.укупно()}")


def главна():
    дирови = [дир for дир in ПУТАЊА_КАТАЛОГА.iterdir() if дир.is_dir() and not дир.name.startswith('__')]
    for дир in дирови:
        фајл_карти = ФајлКарти.учитај(tsv, дир.joinpath('карте.tsv'))
        фајл_записа = ПогледЗаписа(ТабелаЗаписа(дир.joinpath('запис.tsv')))
        Статистика(дир, фајл_карти, фајл_записа).штампај()


if __name__ == '__main__':
    главна()
