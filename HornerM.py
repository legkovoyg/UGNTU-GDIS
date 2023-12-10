import numpy as np
import pandas as pd
import math
import statsmodels.api as sm
from functools import reduce
from array import *


# Сбор информации из Excel файла
def GetInfoFromExcel():
    data = pd.read_excel('in.xlsx')
    return data


# Поиск времени закачки в секундах
def TimeZAK(data, time):
    print('Напишите 1, чтобы выбрать время закачки автоматически')
    print('Напишите 2, чтобы выбрать время закачки самостоятельно')
    choose1 = int(input())
    if choose1 == 1:
        zakach = data.to_numpy(float)[:, -2:]
        for x in zakach:
            if x[1] == 0:
                timeZakSEC = t * 60
                break
            t = x[0]
    if choose1 == 2:
        print('Напишите время закачки в секундах')
        timeZakSEC = int(input())
        for x in time:
            if timeZakSEC < x:
                timeZakSEC = x
                break
    return timeZakSEC


# Расчет массива времени Хорнера
def HornerTime(alltime, DownloadTime):
    HornerTime = []
    for x in alltime:
        if x > DownloadTime:
            addHorner = math.log((x / (x - DownloadTime)))
            HornerTime.append(addHorner)
        else:
            addHorner = 0
            HornerTime.append(addHorner)
    return HornerTime


# Получение массива "закачка-за отрезок времени" (Qdt)
def Qdt(debit, time):
    Qdt = []
    y = 0
    for x in range(0, len(debit)):
        if y == 0:
            b = debit[x] * time[x]
            Qdt.append(b)
            y = y + 1
        else:
            b = debit[x] * (time[x] - time[x - 1])
            Qdt.append(b)
    Qdt = list(filter(lambda i: str(i) != 'nan', Qdt))
    return Qdt


# Весь закачанный объем за время закачки
def FullDebit(Qdt):
    FulDebit = sum(list(Qdt))
    return FulDebit


# Средний дебит за время закачки
def AvgDebit(FullDebit, DownloadTime):
    a = FullDebit
    b = DownloadTime
    AvgDebit = a / b
    return AvgDebit


# Давление после остановки закачки
def GetPressureAfterTest(pressure, alltime, DownloadTime):
    Alldata = pressure, alltime
    Alldata = np.transpose(Alldata)
    PressureAfterTest = []
    for i in Alldata:
        if i[1] > float(DownloadTime):
            PressureAfterTest.append(i[0])
        else:
            continue
    return PressureAfterTest


# Время Хорнера после остановки закачки
def GetHornerAfterTest(HornerTime, alltime, DownloadTime):
    Alldata = HornerTime, alltime
    Alldata = np.transpose(Alldata)
    HornerAfterTest = []
    for i in Alldata:
        if i[1] > float(DownloadTime):
            HornerAfterTest.append(i[0])
        else:
            continue
    return HornerAfterTest


def GetAlltimeAfterTest(alltime, DownloadTime):
    Alldata = alltime
    Alldata = np.transpose(Alldata)
    ALltimeAfterTest = []
    for i in Alldata:
        if i > float(DownloadTime):
            ALltimeAfterTest.append(i)
        else:
            continue
    return ALltimeAfterTest


# Ввод и преобразование пользовательских значений времени Хорнера и давления
def UserHorner(hornerAfterTest, pressureAfterTest):
    Buffer = hornerAfterTest, pressureAfterTest
    Changer = np.transpose(Buffer)
    print('Введите значение времени Хорнера 1, для пластового давления: ')
    userHorner1 = float(input())
    print('Введите значение времени Хорнера 2, для определения пластового давления: ')
    userHorner2 = float(input())
    if userHorner1 > userHorner2:
        userHorner1, userHorner2 = userHorner2, userHorner1
    for x in Changer:
        if userHorner1 > x[0]:
            userHorner1 = x[0]
            userPressure1 = x[1]
            print('Время Хорнера для точки Х1,наиболее приближенное к введенному :', userHorner1)
            print('Давление для точки Х1, наиболее приближенное к введенному:', userPressure1, 'Па')
            break
    for x in Changer:
        if userHorner2 > x[0]:
            userHorner2 = x[0]
            userPressure2 = x[1]
            print('Время Хорнера для точки Х2,наиболее приближенное к введенному :', userHorner2)
            print('Давление для точки Х2, наиболее приближенное к введенному:', userPressure2, 'Па')
            break
    print(userHorner1, userHorner2, userPressure1, userPressure2)
    return userHorner1, userHorner2, userPressure1, userPressure2


# Пластовое давление
def ReservoirPressure(Horner1, Horner2, Pressure1, Pressure2):
    PlastPressure = (Pressure1 - Pressure2) * ((-1) * (Horner2 / (Horner1 - Horner2))) + Pressure1
    print(f'Пластовое давление равно: {PlastPressure}  Па')
    return PlastPressure


# Угол наклона прямой (tga)
def tgAlpha(UserInput):
    tga = (UserInput[3] - UserInput[2]) / (UserInput[1] - UserInput[0])
    print('Уклон касательной равен :', tga)
    return tga


# Гидропроводность
def HydraulicСonductivity(AvgDebit, tga):
    hydro = (AvgDebit / 4 / math.pi / tga) * 10 ** 12
    print('Гидропроводность равна:', hydro, 'м*Д/Па*с')
    return hydro


# Расчет безразмерного времени и давления
def DimensionlessTime(pressure, alltime, thickness, hydro, porosity, compressibility, wellRadius, AvgDebit, coefB):
    a = pressure, alltime
    IterPressure = np.transpose(a)
    New = []
    global iteration_count
    iteration_count = 0
    for x in IterPressure:
        if x[0] < reduce(max, pressure):
            if iteration_count == 0:
                continue
            elif iteration_count == 1:
                New.append([x[0], x[1]])
        elif x[0] == reduce(max, pressure):
            New.append([x[0], x[1]])
            iteration_count = 1
    startTime = float(New[0][1])
    tD = []

    for x in New:
        if x[1] - startTime == 0:
            tD.append(0)
        else:
            td1 = 0.0002637 * hydro * (x[1] - startTime)
            td2 = (porosity * compressibility * math.pow(wellRadius, 2) * thickness * 3600)
            td = td1 / td2
            tD.append(td)

    startPressure = float(New[0][0])
    pwD = []
    for x in New:
        if x[0] - startPressure == 0:
            pwD.append(0)
        else:
            pwd1 = hydro / (141.2 * AvgDebit * coefB)
            pwd2 = ((startPressure - x[0]) * 0.00015)
            pwd = pwd1 * pwd2
            pwD.append(pwd)
    return tD, pwD


# Производная безразмерного давления
def pwDtotD(tD, pwD):
    dx = np.diff(tD)
    dy = np.diff(pwD)
    dxdy = np.transpose([dx, dy])
    result = []
    for x in dxdy:
        result1 = x[1] / x[0]
        result.append(result1)
    return result


# Экспоненциальное сглаживание производной безразмерного давления
def exponential_smoothing(series, alpha):
    result = [series[0]]
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n - 1])
    return result


# mest
def Mest(pwd, td):
    ds = np.transpose([td, pwd])
    print('Введите количество точек, которые необходимо выбрать: ')
    n = int(input())
    indices = []
    for i in range(0, n):
        print('Введите индексы точек, которые необходимо выбрать.')
        b = int(input())
        indices.append(b)
    selected_points = [ds[index] for index in indices]
    df = pd.DataFrame(selected_points)
    x = df.values[:, 0]
    y = df.values[:, 1]
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    mestK = model.params[1]
    mestB = model.params[0]
    return mestK, mestB


# Максимальное значение производной безразмерного давления и соответствующее значение безразмерного времени
def getMax(exponental, twd):
    Max = np.transpose([exponental, twd])
    for x in Max:
        if x[0] == max(exponental):
            expMax = x[0]
            twdMax = x[1]
    return expMax, twdMax


# С коэф
def Ccoef(q, exponental, B, tmax):
    C = (2 * q * exponental * B) / (tmax * 24 * math.exp(2))
    return C


# CD коэф
def CDcoef(Ccoef, porosity, compressibility, wellRadius):
    CD = (Ccoef / (porosity * compressibility * wellRadius ** 2))
    print(f'Ccoef', Ccoef,
          f'porosity', porosity,
          f'compressibility', compressibility,
          f'wellRadius', wellRadius)
    print(CD)
    return CD


# Скин-фактор
def Skin(debit, B, C, hydro, tzak, mest, CD):
    Skin = ((debit * hydro * B * tzak * 0.02061405) / ((C ** 2) * mest)) - math.log(CD * 1.9959675 * (10 ** 6)) / 2
    print(f'debit', debit,
          f'B', B,
          f'C', C,
          f'hydro', hydro,
          f'tzak', tzak,
          f'mest', mest,
          f'CD', CD)
    print(Skin)
    return Skin
