import numpy as np
import pandas as pd
import math

from classes import Pressure, Time, Debit


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
# def ReservoirPressure(UserInput):
#     PlastPressure = (UserInput[2] - UserInput[3]) * ((-1) * (UserInput[1] / (UserInput[0] - UserInput[1]))) + UserInput[
#         3]
#     print(f'Пластовое давление равно: {PlastPressure}  Па')
#     return PlastPressure

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
