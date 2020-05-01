from pathlib import Path
from наки.tsv import Табела, ЗаглављеГрешка, ПарсирањеГрешка


class ТестТабела(Табела):
    def __init__(бре, путања, Тип, на_диску):
        super().__init__(путања, Тип)
        бре._на_диску = на_диску

    def _учитај(бре, путања, Тип):
        assert isinstance(путања, Path), путања
        елементи = []
        for и, ред in enumerate(бре._на_диску, 1):
            if и == 1:
                заг = Тип.заглавље()
                if ред != заг:
                    raise ЗаглављеГрешка(f"Заглавље се не поклапа: {заг} {ред}")
            else:
                if not ред:
                    continue
                try:
                    елементи.append(Тип.елемент(ред))
                except Exception as е:
                    raise ПарсирањеГрешка(f'(линија:{и}){ред}') from е
        return елементи

    def _додај(бре, путања, Тип, елементи):
        assert isinstance(путања, Path), путања
        додај_заглавље = False
        if бре._на_диску:
            ред = бре._на_диску[0]
            заг = Тип.заглавље()
            if ред != заг:
                raise ЗаглављеГрешка(f"Заглавље се не поклапа: {заг} {ред}")
        else:
            додај_заглавље = True
        if додај_заглавље:
            бре._на_диску.append(Тип.заглавље())
        for елемент in елементи:
            бре._на_диску.append(Тип.ред(елемент))

