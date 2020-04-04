import sys
import uuid


def главни(фајл):
    with open(фајл, 'rb') as ф:
        дата = ф.read()
        for слог in дата.split(b'\x0a'):
            with open(uuid.uuid4().hex + '.txt', 'w') as блоб:
                блоб.write(слог.decode('utf-8'))


if __name__ == '__main__':
    главни(sys.argv[1])
