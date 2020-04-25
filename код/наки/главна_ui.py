from наки.ui import UI


class ГлавнаUI(UI):
    def __init__(бре, терминал, регистар):
        super().__init__(терминал, регистар)

    def одабери_шпил(бре, листа, опис):
        with бре.т.пун_екран():
            while True:
                бре.т.обриши()
                with бре.т.статус():
                    бре._принт_сепаратор('=')
                    if isinstance(опис, list):
                        for о in опис:
                            бре.т.принт(о)
                    else:
                        бре.т.принт(опис)
                with бре.т.главни():
                    бре._принт_листа(листа)
                    индекс = бре.т.инпут('#? ').strip()
                    if бре._регистар.изврши(индекс, индекс=индекс):
                        return
                    бре.т.звук_грешке()

    def _принт_листа(бре, листа):
        for индекс, елемент in enumerate(листа, 1):
            бре.т.принт(f"{индекс}) {елемент}")

