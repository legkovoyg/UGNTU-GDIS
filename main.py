import numpy as np
import HornerM
from Graphics import FirstGraphic, SecondGraphic, ThirdGraphic
from classes import Pressure, Time, Debit, Meters, Hydro, Compressibility

# Все данные из Excel файла
data = HornerM.GetInfoFromExcel()
# Все время исследования
alltime = data.to_numpy(float)[:, 0]
alltime = Time(alltime).fMin_toSec
# Забойное давление
pressure = data.to_numpy(float)[:, 1]
pressure = Pressure(pressure).fATM_toPa
# Значение времени во время закачки
time = data.to_numpy(float)[:, 2]
time = Time(time).fMin_toSec
# Изменение объема закачки во времени
debit = data.to_numpy(float)[:, 3]
debit = Debit(debit).fM3min_toM3sec
# Время остановки закачки
DownloadTime = HornerM.TimeZAK(data, time)
# Время Хорнера
HornerTime = HornerM.HornerTime(alltime, DownloadTime)
# Qdt
Qdt = HornerM.Qdt(debit, time)
# Объем закачанной жидкости
SumOfDebit = HornerM.FullDebit(Qdt)
# Средний дебит за время закачки
AvgDebit = HornerM.AvgDebit(SumOfDebit, DownloadTime)
# График t - Pзаб
FirstGraphic(pressure, alltime, debit)
# Давление после остановки закачки
pressureAfterTest = HornerM.GetPressureAfterTest(pressure,
                                                 alltime,
                                                 DownloadTime)
# Время Хорнера после остановки закачки
hornerAfterTest = HornerM.GetHornerAfterTest(HornerTime,
                                             alltime,
                                             DownloadTime)
alltimeAfterTest = HornerM.GetAlltimeAfterTest(alltime, DownloadTime)
# График Время Хорнера - Pзаб
SecondGraphic(hornerAfterTest, pressureAfterTest)
# Обработка параметров вводимых пользователем
UserInput = HornerM.UserHorner(hornerAfterTest, pressureAfterTest)
# Расчет пластового давления
PlastPressure = HornerM.ReservoirPressure(UserInput[0],
                                          UserInput[1],
                                          UserInput[2],
                                          UserInput[3])
# Угол наклона прямой (tga)
tga = HornerM.tgAlpha(UserInput)
# Гидропроводность
HydConductivity = HornerM.HydraulicСonductivity(AvgDebit, tga)
print('Введите толщину пласта, м')
# PlastThickness = input()
PlastThickness = 8.0

print('Введите величину коэффициента B, безразмерное')
# coefB = input()
coefB = 1.2
print('Введите значение пористости, д.ед ')
# Porosity = input()
Porosity = 0.28
print('Введите значение сжимаемости нефти')
# compressibility = float(input())
compressibility = 0.01
print('Введите значение радиуса скважины, м')
# WellRadius = input()
WellRadius = 0.146

DimensTime = HornerM.DimensionlessTime(pressureAfterTest,
                                       alltimeAfterTest,
                                       Meters(PlastThickness).fM_toFoot,
                                       Hydro(HydConductivity).fDarsi_toFoot,
                                       Porosity,
                                       Compressibility(compressibility).fSI_toAmer,
                                       Meters(WellRadius).fM_toFoot,
                                       Debit(AvgDebit).fM3sec_toSTBd,
                                       coefB)[0]

DimensPressure = HornerM.DimensionlessTime(pressureAfterTest,
                                           alltimeAfterTest,
                                           Meters(PlastThickness).fM_toFoot,
                                           Hydro(HydConductivity).fDarsi_toFoot,
                                           Porosity,
                                           Compressibility(compressibility).fSI_toAmer,
                                           Meters(WellRadius).fM_toFoot,
                                           Debit(AvgDebit).fM3sec_toSTBd,
                                           coefB)[1]

dPWDtodTD = HornerM.pwDtotD(DimensTime, DimensPressure)
exponental = HornerM.exponential_smoothing(dPWDtodTD, 0.2)
ThirdGraphic(DimensTime, DimensPressure, dPWDtodTD, exponental)
