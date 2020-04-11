import os
import sys
import subprocess
import readchar
from blessings import Terminal

УРЕЗ = ' ' * 40
БОЈА_СИВА = 7


class Терминал():

    def __init__(бре):
        бре.т = Terminal()

    def пун_екран(бре):
        return бре.т.fullscreen()

    def сакривен_курсор(бре):
        return бре.т.hidden_cursor()

    def главни(бре):
        return бре.т.location(0, 9)

    def статус(бре):
        return бре.т.location(0, бре.т.height-9)

    def инпут(бре, текст):
        return input(УРЕЗ + текст)

    def инпут_код(бре):
        return readchar.readkey()

    def обриши(бре):
        print(бре.т.clear)

    def звук_грешке(бре):
        print('\a', end='', flush=True)

    def принт(бре, *args, **kw):
        print(УРЕЗ, end='')
        print(*args, **kw)

    def принт_зелено(бре, текст):
        бре.принт(бре.т.green(текст))

    def принт_плаво(бре, текст):
        бре.принт(бре.т.blue(текст))

    def принт_сиво(бре, текст):
        бре.принт(бре.т.color(БОЈА_СИВА) + текст + бре.т.normal)

    def формат_мд(бре, текст):
        """ текст са [болд] и {плавим} нагласцима """
        текст = текст.replace('[[', 'ДУПЛЕ_КОЦКАСТЕ_ЛЕВЕ').replace(']]', 'ДУПЛЕ_КОЦКАСТЕ_ДЕСНЕ')
        текст = текст.replace('[', 'ЈЕДНА_КОЦКАСТА_ЛЕВА').replace(']', 'ЈЕДНА_КОЦКАСТА_ДЕСНА')
        текст = текст.replace('{{{', 'ТРОСТРУКЕ_ВИТИЧАСТЕ_ЛЕВЕ').replace('}}}', 'ТРОСТРУКЕ_ВИТИЧАСТЕ_ДЕСНЕ')
        текст = текст.replace('{{', 'ДУПЛЕ_ВИТИЧАСТЕ_ЛЕВЕ').replace('}}', 'ДУПЛЕ_ВИТИЧАСТЕ_ДЕСНЕ')
        текст = текст.replace('{', 'ЈЕДНА_ВИТИЧАСТА_ЛЕВА').replace('}', 'ЈЕДНА_ВИТИЧАСТА_ДЕСНА')
        текст = текст.replace('ДУПЛЕ_КОЦКАСТЕ_ЛЕВЕ', '[').replace('ДУПЛЕ_КОЦКАСТЕ_ДЕСНЕ', ']')
        текст = текст.replace('ДУПЛЕ_ВИТИЧАСТЕ_ЛЕВЕ', '{').replace('ДУПЛЕ_ВИТИЧАСТЕ_ДЕСНЕ', '}')
        текст = текст.replace('ЈЕДНА_КОЦКАСТА_ЛЕВА', бре.т.bold).replace('ЈЕДНА_КОЦКАСТА_ДЕСНА', бре.т.normal)
        текст = текст.replace('ЈЕДНА_ВИТИЧАСТА_ЛЕВА', бре.т.blue).replace('ЈЕДНА_ВИТИЧАСТА_ДЕСНА', бре.т.normal)
        текст = текст.replace('ТРОСТРУКЕ_ВИТИЧАСТЕ_ЛЕВЕ', бре.т.blue + '{')
        текст = текст.replace('ТРОСТРУКЕ_ВИТИЧАСТЕ_ДЕСНЕ', '}' + бре.т.normal)
        return текст

    def отвори_урл(бре, урл):
        if not урл:
            бре.звук_грешке()
            return
        if sys.platform == 'win32':
            os.startfile(урл)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', урл])
        else:
            subprocess.Popen(['xdg-open', урл])

    def измени(бре, права_путања, линија):
        subprocess.run(['vim', '+' + линија, '+normal_WW', str(права_путања)])
