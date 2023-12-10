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
        self.fMin_toMin = x
        self.fMin_toSec = [i * 60 for i in x]
        self.fMin_toHour = [i * 3600 for i in x]


class Debit:
    def __init__(self, x):
        self.fM3min_toM3min = x
        self.fM3min_toM3sec = x / 60
        self.fM3min_toM3hour = x * 60
        self.fM3sec_toSTBd = x * 543439


class Meters:
    def __init__(self, x):
        self.fM_toFoot = x * 3.28


class Hydro:
    def __init__(self, x):
        self.fDarsi_toDarsi = x
        self.fDarsi_toM2 = x * (10 ** (-12))
        self.fDarsi_toFoot = x * 3.28
        self.fM2_toFoot = (x / (10 ** (-12)) * 3.28)


class Compressibility:
    def __init__(self, x):
        self.fSI_toAmer = x / 145.037737730006
