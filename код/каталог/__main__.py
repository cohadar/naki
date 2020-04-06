from наки import tsv
from наки.конфигурација import ПУТАЊА_КАТАЛОГА
from наки.карте import Карта, Линк


def одради_дир(дир, извор_учитај, извор_одради):
    карте = []
    линкови = []
    извор_дир = дир.joinpath('извор')
    for извор_фајл in sorted(ф for ф in извор_дир.iterdir() if ф.is_file()):
        лепа_путања = дир.name + '/извор/' + извор_фајл.name
        print(лепа_путања)
        извор = извор_учитај(извор_фајл)
        к, л = извор_одради(лепа_путања, извор)
        карте.extend(к)
        линкови.extend(л)
    tsv.препиши_фајл(дир.joinpath('карте.tsv'), Карта, карте)
    if линкови:
        tsv.препиши_фајл(дир.joinpath('линкови.tsv'), Линк, линкови)


def одради_шпил(шпил):
    име_шпила = шпил.name
    if име_шпила in ["de_Basic", "de_Präteritum"]:
        from каталог.извори.de_basic import извор_учитај, извор_одради
    elif име_шпила in ["de_Verben"]:
        from каталог.извори.de_verben import извор_учитај, извор_одради
    elif име_шпила == "de_Nomen":
        from каталог.извори.de_nomen import извор_учитај, извор_одради
    elif име_шпила == "de_Und":
        from каталог.извори.de_und import извор_учитај, извор_одради
    elif име_шпила == "de_Cloze":
        from каталог.извори.de_cloze import извор_учитај, извор_одради
    elif име_шпила in ["de_Einweg", "чворови"]:
        from каталог.извори.de_einweg import извор_учитај, извор_одради
    elif име_шпила == "песме":
        from каталог.извори.песме import извор_учитај, извор_одради
    elif име_шпила.startswith("тест_"):
        from каталог.извори.тест_дата_генератор import извор_учитај, извор_одради
    else:
        raise Exception(f"Некатегоризован шпил: {име_шпила}")
    одради_дир(шпил, извор_учитај, извор_одради)


def главна():
    шпилови = sorted([шпил for шпил in ПУТАЊА_КАТАЛОГА.iterdir() if шпил.is_dir() and not шпил.name.startswith('__')])
    for шпил in шпилови:
        одради_шпил(шпил)


if __name__ == '__main__':
    главна()
