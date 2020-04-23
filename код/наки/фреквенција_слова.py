import sys
from collections import Counter


def главна():
    фрек = Counter()
    for линија in sys.stdin:
        for слово in линија:
            фрек[слово] += 1
    парови = фрек.items()
    парови = sorted(парови, key=lambda т: т[1], reverse=True)
    for пар in парови:
        print(пар[0], пар[1])


if __name__ == '__main__':
    главна()
