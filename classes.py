class Pressure:
    def __init__(self, x):
        self.fATM_toATM = x
        self.fATM_toMPa = [num / 9.869 for num in x]
        self.fATM_toPa = [num * 101327.3887931908 for num in x]
        self.fPa_toATM = [num / 101327.3887931908 for num in x]
        self.fPa_toMPa = [num / (10 ** 6) for num in x]
        self.fPa_toPa = x


class Time:
    def __init__(self, x):
        self.min = x
        self.sec = [i * 60 for i in x]
        self.hour = [i * 3600 for i in x]


class Debit:
    def __init__(self, x):
        self.m3min = x
        self.m3sec = [i / 60 for i in x]
        self.m3hour = [i * 60 for i in x]
