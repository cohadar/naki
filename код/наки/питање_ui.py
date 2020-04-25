from наки.команда import КОМАНДА_ФЕЈЛ, КОМАНДА_ПЛУС1, КОМАНДА_ПЛУС2
from наки.ui import UI


class ПитањеUI(UI):
    def __init__(бре, терминал, регистар):
        super().__init__(терминал, регистар)
        бре._претходни_текст = None
        бре._зелено = False

    def _принт_мд(бре, текст):
        """ принт маркдовн текст """
        assert текст is not None
        for т in бре.т.формат_мд(текст).split('\\n'):
            бре.т.принт(т)

    def _принт_наслов(бре, текст):
        промена_врсте = False
        if бре._претходни_текст is None:
            бре._претходни_текст = текст
        if бре._претходни_текст != текст:
            бре._зелено = not бре._зелено
            промена_врсте = True
        бре._претходни_текст = текст
        if бре._зелено:
            бре.т.принт_зелено(текст)
        else:
            бре.т.принт_плаво(текст)
        бре.т.принт()
        return промена_врсте

    def _принт_сепаратор(бре, c, број=None):
        if број is None:
            бре.т.принт_сиво(c * 60)
        else:
            бре.т.принт_сиво((c * 1) + f"[{број}]" + (c * (59 - len(f"[{број}]"))))

    def _принт_питање(бре, наслов, питање, број_преосталих_карата):
        промена_врсте = бре._принт_наслов(наслов)
        бре._принт_мд(питање)
        бре._принт_сепаратор('-')
        with бре.т.статус():
            бре._принт_сепаратор('=', број_преосталих_карата)
            бре.т.принт('притисни било који тастер')
        return промена_врсте

    def питање(бре, дата, наслов, питање, број_преосталих_карата):
        with бре.т.пун_екран():
            with бре.т.сакривен_курсор():
                бре.т.обриши()
                with бре.т.главни():
                    промена_врсте = бре._принт_питање(наслов, питање, број_преосталих_карата)
                    к = бре.т.инпут_код()
                    if промена_врсте:
                        if к in КОМАНДА_ФЕЈЛ or к in КОМАНДА_ПЛУС1 or к in КОМАНДА_ПЛУС2:
                            бре.т.звук_грешке()
                            бре._претходни_текст = 'magic98012741041041923841902492410'
                            return False
                    return not бре._регистар.изврши(к, **дата)

    def отвори_урл(бре, урл):
        бре.т.отвори_урл(урл)

    def измени(бре, путања, линија):
        бре.т.измени(путања, линија)

    def додај_нa_извор(бре, путања):
        бре.т.додај_на_извор(путања)

