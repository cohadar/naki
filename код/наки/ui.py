from наки.команда import КОМАНДА_ПРЕКИД, КОМАНДА_ОТВОРИ_УРЛ, КОМАНДА_ЕДИТУЈ
from наки.команда import КОМАНДА_ФЕЈЛ, КОМАНДА_ПЛУС1, КОМАНДА_ПЛУС2


class UI():
    def __init__(бре, терминал):
        бре.т = терминал
        бре.акције = {}

    def региструј_акцију(бре, команда, акција, објекат):
        if бре.акције.get(команда) is not None:
            raise ValueError(f"Команда већ регистрована: {команда}")
        бре.акције[команда] = (акција, објекат)

    def изврши_акцију(бре, команда, дата):
        пар = бре.акције.get(команда, None)
        if пар is None:
            raise ValueError(f"Нерегистрована команда: {команда}")
        акција, објекат = пар
        акција(објекат, дата)

    def одабери_шпил(бре, листа, опис, регистар):
        while True:
            бре.т.обриши()
            with бре.т.статус():
                бре.т.принт_сепаратор('=')
                if isinstance(опис, list):
                    for о in опис:
                        бре.т.принт(о)
                else:
                    бре.т.принт(опис)
            with бре.т.главни():
                бре.т.принт_листа(листа)
                индекс = бре.т.инпут('#? ').strip()
                if регистар.изврши(индекс):
                    return
                бре.т.звук_грешке()

    def _измени(бре, путања_каталога, лепа_путања, линија):
        права_путања = путања_каталога.joinpath(лепа_путања)
        бре.т.измени(права_путања, линија)

    def _принт_питање(бре, наслов, питање, број_преосталих_карата):
        бре.т.принт_наслов(наслов)
        бре.т.принт_мд(питање)
        бре.т.принт_сепаратор('-')
        with бре.т.статус():
            бре.т.принт_сепаратор('=', број_преосталих_карата)
            бре.т.принт('притисни било који тастер')

    def питање_и_одговор(бре, путања_каталога, наслов, питање, одговор, извор, линија, број_преосталих_карата, урл):
        бре.т.обриши()
        with бре.т.главни():
            бре._принт_питање(наслов, питање, број_преосталих_карата)
            while True:
                к = бре.т.инпут_код()
                if к in КОМАНДА_ПРЕКИД:
                    return (True, None)
                if к in КОМАНДА_ОТВОРИ_УРЛ:
                    if урл:
                        бре.т.отвори_урл(урл)
                    else:
                        бре.т.звук_грешке()
                    continue
                if к in КОМАНДА_ЕДИТУЈ:
                    бре._измени(путања_каталога, извор, линија)
                    continue
                break
            бре.т.принт_мд(одговор)
            with бре.т.статус():
                бре.т.принт_сепаратор('=', број_преосталих_карата)
                бре.т.принт('оцени одговор (f: 0)(space: +1)(enter: +2)')
            ДОЗВОЉЕНЕ = [КОМАНДА_ПРЕКИД, КОМАНДА_ОТВОРИ_УРЛ, КОМАНДА_ЕДИТУЈ, КОМАНДА_ФЕЈЛ, КОМАНДА_ПЛУС1, КОМАНДА_ПЛУС2]

            def екстра(и):
                for к in ДОЗВОЉЕНЕ:
                    if и in к:
                        return к
                return None

            while True:
                к = бре.т.инпут_код(екстра)
                if к in КОМАНДА_ПРЕКИД:
                    return (True, None)
                elif к in КОМАНДА_ОТВОРИ_УРЛ:
                    if урл:
                        бре.т.отвори_урл(урл)
                    else:
                        бре.т.звук_грешке()
                    continue
                elif к in КОМАНДА_ЕДИТУЈ:
                    бре._измени(путања_каталога, извор, линија)
                    continue
                elif к in КОМАНДА_ФЕЈЛ:
                    return (False, 0)
                elif к in КОМАНДА_ПЛУС1:
                    return (False, 1)
                elif к in КОМАНДА_ПЛУС2:
                    return (False, 2)
                else:
                    raise Exception(f'непозната команда: {к}')
