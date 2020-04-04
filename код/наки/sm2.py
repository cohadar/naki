import attr


def days(n):
    r = ''
    if n >= 365:
        r += (str(n // 365) + 'y')
        n %= 365
    if n >= 30:
        r += (str(n // 30) + 'm')
        n %= 30
    if n > 0 or r == '':
        r += (str(n) + 'd')
    return r


@attr.s
class SM2():
    n = attr.ib(default=1)
    ef = attr.ib(default=2.5)
    prev = attr.ib(default=0)

    def __call__(self, q):
        assert q in range(6)
        print(f'n = {self.n}, ef = {round(self.ef, 2)}, interval = {days(self.prev)}')
        prev_ = self._interval()
        self._new_ef(q)
        if q < 3:
            self.n = 1
        else:
            self.n += 1
            self.prev = prev_

    def _interval(self):
        assert self.n > 0
        if self.n == 1:
            return 1
        if self.n == 2:
            return 6
        return round(self.prev * self.ef)

    def _new_ef(self, q):
        self.ef = self.ef + (0.1-(5-q)*(0.08+(5-q)*0.02))
        if self.ef < 1.3:
            self.ef = 1.3


@attr.s
class Mighty():
    n = attr.ib(default=1)
    ef = attr.ib(default=2.5)
    prev = attr.ib(default=1)
    cumul = attr.ib(default=0)

    def __call__(self, q):
        assert q in range(6)
        self.prev = self._interval()
        # self._new_ef(q)
        self.cumul += self.prev
        print(f'n = {self.n}, ef = {round(self.ef, 2)}, interval = {days(self.prev)}, cumul={days(self.cumul)}')
        self.n += 1

    def _interval(self):
        assert self.n > 0
        if self.n == 1:
            return 1
        if self.n == 2:
            return 6
        return round(self.prev * self.ef)

    def _new_ef(self, q):
        x = [0, 1.97, 3.55, 2.5]
        self.ef = x[q]


def main():
    # 365 122 41 14 5 1 0
    # 2.5 1.46 1.27
    algo = Mighty()
    qz = [1 for _ in range(9)]
    # x5 = [5,5,5,2,2,2,5,5,5,5,2,5,2,5,2,5,2,5,2,5,2,5,2,5,2,5,2,5,2,5]
    while True:
        for q in qz:
            algo(q)
        algo.ef = float(input("ef? "))
        algo.n = 1
        algo.prev = 1
        algo.cumul = 0


if __name__ == '__main__':
    main()
