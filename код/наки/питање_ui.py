from наки.команда import КОМАНДА_ФЕЈЛ, КОМАНДА_ПЛУС1, КОМАНДА_ПЛУС2
from наки.ui import UI


class ПитањеUI(UI):
    def __init__(бре, стање, терминал, регистар):
        super().__init__(терминал, регистар)
        бре.стање = стање

    def питање(бре, дата, наслов, питање, број_преосталих_карата):
        with бре.т.пун_екран():
            with бре.т.сакривен_курсор():
                бре.т.обриши()
                with бре.т.главни():
                    промена_наслова = бре._принт_наслов(наслов)
                    бре._принт_питање(питање, број_преосталих_карата)
                    к = бре.т.инпут_код()
                    if промена_наслова:
                        if к in КОМАНДА_ФЕЈЛ or к in КОМАНДА_ПЛУС1 or к in КОМАНДА_ПЛУС2:
                            бре.т.звук_грешке()
                            бре.стање.претходни_текст = 'magic98012741041041923841902492410'
                            return False
                    return not бре._регистар.изврши(к, **дата)

