import sys
import time
import datetime


def main():
    for i in sys.stdin:
        s = i.split('-')
        d = datetime.date(int(s[0]), int(s[1]), 1)
        t = time.mktime(d.timetuple())
        print(int(t))


if __name__ == '__main__':
    main()
